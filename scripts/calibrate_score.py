#!/usr/bin/env python3
"""Calibracao empirica dos pesos do GEO Score Checker contra Papers.

Este script implementa a ponte estatistica entre os dois projetos GEO:

  - Papers fornece o GROUND TRUTH: para cada (dominio, vertical), a taxa
    empirica de citacao em N queries reais executadas contra os 4 LLMs.
  - GEO Score Checker fornece o vetor de FEATURES: 8 dimensoes
    (D1..D8) extraidas a partir de probes HTTP, JSON-LD, LLM ping etc.

A juncao das duas fontes vive na tabela score_calibration_inputs e e o
dataset (D, y) sobre o qual ajustamos uma regressao logistica:

    logit(P(cited|site)) = beta0 + sum_d beta_d * D_d

Os pesos w*_d do Score Checker passam a ser estimados:

    w*_d = 100 * max(0, beta_d) / sum_k max(0, beta_k)

substituindo os pesos cravados (15, 15, 20, 15, 10, 10, 10, 5).

O script reporta:
  - Coeficientes, odds ratios, p-valores
  - AUROC (discriminacao) via 5-fold CV
  - Brier score e reliability diagram (calibracao)
  - Pesos calibrados normalizados para somar 100
  - JSON consumivel pelo dashboard

Uso:
    python scripts/calibrate_score.py                    # le do banco real
    python scripts/calibrate_score.py --simulate 200     # gera dataset sintetico
    python scripts/calibrate_score.py --output out.json  # salva em arquivo
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

# Permite rodar tanto via "python scripts/calibrate_score.py" quanto via modulo
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis.statistical import StatisticalAnalyzer  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("calibrate_score")


# ----------------------------------------------------------------------
# Pesos atuais do GEO Score Checker (espelhando score-calculator.ts)
# ----------------------------------------------------------------------

CURRENT_WEIGHTS: dict[str, float] = {
    "d1_retrieval_fitness": 15.0,
    "d2_reranking_fitness": 15.0,
    "d3_generation_exposure": 20.0,
    "d4_faithful_credit": 15.0,
    "d5_answer_bubble_consensus": 10.0,
    "d6_geo_robustness": 10.0,
    "d7_static_readiness": 10.0,
    "d8_entity_authority": 5.0,
}
DIMS = list(CURRENT_WEIGHTS.keys())

DB_PATH = os.getenv("PAPERS_DB_PATH", str(ROOT / "data" / "papers.db"))


# ----------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------

def load_dataset_from_db(db_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Load (X, y, n) from score_calibration_inputs table.

    y aqui e a taxa de citacao empirica (proporcao). Para a regressao
    logistica usaremos um logit ponderado: cada linha conta como n_observations
    realizacoes Bernoulli (k_cited sucessos), respeitando a verossimilhanca
    binomial.

    Returns:
        X (N, 8): matriz de features
        k (N,)  : sucessos por linha
        n (N,)  : tamanho de amostra por linha
        domains (N,): identificadores
    """
    if not Path(db_path).exists():
        raise FileNotFoundError(f"DB nao encontrado: {db_path}")
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(f"""
            SELECT domain, k_cited, n_observations,
                   {', '.join(DIMS)}
              FROM score_calibration_inputs
             ORDER BY collected_at DESC
        """)
        rows = cur.fetchall()
    finally:
        conn.close()
    if not rows:
        return np.empty((0, len(DIMS))), np.array([]), np.array([]), []
    X = np.array([list(r[3:]) for r in rows], dtype=float)
    k = np.array([r[1] for r in rows], dtype=float)
    n = np.array([r[2] for r in rows], dtype=float)
    domains = [r[0] for r in rows]
    return X, k, n, domains


def simulate_dataset(n_samples: int = 200, seed: int = 7) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Gera um dataset sintetico plausivel para uma demonstracao end-to-end.

    Modelo gerador (DAG conhecido):
        D ~ U[0,1]^8
        true beta (latente, NAO os pesos atuais):
            beta_true = [+2.5, +2.0, +3.5, +1.8, +0.6, +0.4, +1.0, +0.3]
        eta = -2.0 + D @ beta_true
        p   = sigmoid(eta)
        n   ~ Poisson(40) + 10
        k   ~ Binomial(n, p)

    O ponto deste exercicio sintetico e mostrar que a calibracao recupera
    pesos PROPORCIONAIS aos beta_true (em valor absoluto), e portanto
    diferentes dos pesos cravados atuais (15, 15, 20, 15, 10, 10, 10, 5).
    """
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 1, size=(n_samples, len(DIMS)))
    beta_true = np.array([2.5, 2.0, 3.5, 1.8, 0.6, 0.4, 1.0, 0.3])
    intercept = -2.0
    eta = intercept + X @ beta_true
    p = 1.0 / (1.0 + np.exp(-eta))
    n = rng.poisson(40, size=n_samples) + 10
    k = rng.binomial(n.astype(int), p)
    domains = [f"sim_{i:04d}.example" for i in range(n_samples)]
    return X.astype(float), k.astype(float), n.astype(float), domains


# ----------------------------------------------------------------------
# Logistic regression (binomial via expanded Bernoulli)
# ----------------------------------------------------------------------

def expand_to_bernoulli(
    X: np.ndarray, k: np.ndarray, n: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Expande (X, k, n) para Bernoulli individual.

    Para cada linha i, replicamos X_i n_i vezes; das quais k_i recebem y=1.
    Trade-off: aumenta o tamanho do dataset mas permite usar Logit padrao
    sem precisar trocar para GLM(Binomial). Para n_i moderado (~50) e
    n_samples ~200, ainda fica em ~10k linhas — trivial.
    """
    Xs: list[np.ndarray] = []
    ys: list[float] = []
    for i in range(X.shape[0]):
        ni = int(n[i])
        ki = int(k[i])
        if ni <= 0:
            continue
        Xs.append(np.tile(X[i], (ni, 1)))
        row_y = np.zeros(ni, dtype=float)
        row_y[:ki] = 1.0
        ys.append(row_y)
    if not Xs:
        return np.empty((0, X.shape[1])), np.empty((0,))
    return np.vstack(Xs), np.concatenate(ys)


def fit_logit(X_b: np.ndarray, y_b: np.ndarray) -> dict[str, Any]:
    """Fit a logistic regression and return diagnostics.

    Retorna coeficientes, odds ratios, p-valores e AIC/BIC. Em caso de
    falha de convergencia (separacao perfeita, etc.), retorna converged=False.
    """
    try:
        import statsmodels.api as sm
        from statsmodels.discrete.discrete_model import Logit
    except ImportError:
        return {"converged": False, "error": "statsmodels nao instalado"}

    Xc = sm.add_constant(X_b)
    try:
        model = Logit(y_b, Xc).fit(disp=0, maxiter=200)
    except Exception as exc:
        return {"converged": False, "error": str(exc)}

    coefs = {
        DIMS[i]: {
            "beta": float(model.params[i + 1]),
            "p_value": float(model.pvalues[i + 1]),
            "odds_ratio": float(np.exp(model.params[i + 1])),
            "ci_low_95": float(model.conf_int()[i + 1][0]),
            "ci_high_95": float(model.conf_int()[i + 1][1]),
            "significant": bool(model.pvalues[i + 1] < 0.05),
        }
        for i in range(len(DIMS))
    }
    return {
        "converged": True,
        "intercept": float(model.params[0]),
        "intercept_p": float(model.pvalues[0]),
        "pseudo_r2_mcfadden": float(model.prsquared),
        "llr_p_value": float(model.llr_pvalue),
        "aic": float(model.aic),
        "bic": float(model.bic),
        "n_observations": int(len(y_b)),
        "coefficients": coefs,
        "_model_obj": model,  # consumido downstream e removido antes do dump
    }


def compute_calibrated_weights(coefficients: dict[str, dict[str, Any]]) -> dict[str, float]:
    """Map fitted betas to weights summing to 100.

    Estrategia conservadora:
      - so coeficientes positivos contribuem (uma dimensao com beta < 0
        viola a hipotese de design e nao deveria pesar);
      - coeficientes positivos sao normalizados para somar 100.

    Se TODOS os betas forem negativos, retorna pesos uniformes (12.5 cada),
    sinalizando "modelo nao informativo".
    """
    pos = {dim: max(0.0, c["beta"]) for dim, c in coefficients.items()}
    total = sum(pos.values())
    if total < 1e-9:
        return {dim: round(100 / len(DIMS), 2) for dim in DIMS}
    return {dim: round(100 * pos[dim] / total, 2) for dim in DIMS}


# ----------------------------------------------------------------------
# Cross-validation (5-fold) para AUROC
# ----------------------------------------------------------------------

def auroc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """AUROC via formula de Mann-Whitney (sem dependencia de sklearn)."""
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    # Conta pares concordantes
    n_pos = len(pos)
    n_neg = len(neg)
    # Ranking
    all_scores = np.concatenate([pos, neg])
    order = np.argsort(all_scores, kind="mergesort")
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(all_scores) + 1)
    # Empates: media de ranks
    _, inverse, counts = np.unique(all_scores, return_inverse=True, return_counts=True)
    if (counts > 1).any():
        for u in np.unique(inverse):
            mask = inverse == u
            ranks[mask] = ranks[mask].mean()
    sum_ranks_pos = ranks[:n_pos].sum()
    u_stat = sum_ranks_pos - n_pos * (n_pos + 1) / 2.0
    return float(u_stat / (n_pos * n_neg))


def cv_auroc(
    X: np.ndarray, y: np.ndarray, k_folds: int = 5, seed: int = 42
) -> dict[str, float]:
    """5-fold CV para AUROC + Brier."""
    try:
        import statsmodels.api as sm
        from statsmodels.discrete.discrete_model import Logit
    except ImportError:
        return {"auroc": float("nan"), "brier": float("nan"), "error": "statsmodels missing"}
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y))
    rng.shuffle(idx)
    folds = np.array_split(idx, k_folds)
    aurocs: list[float] = []
    briers: list[float] = []
    for f in range(k_folds):
        test_idx = folds[f]
        train_idx = np.concatenate([folds[g] for g in range(k_folds) if g != f])
        Xt = sm.add_constant(X[train_idx])
        try:
            mdl = Logit(y[train_idx], Xt).fit(disp=0, maxiter=200)
        except Exception:
            continue
        Xv = sm.add_constant(X[test_idx])
        p_pred = mdl.predict(Xv)
        a = auroc(y[test_idx], p_pred)
        b = float(np.mean((p_pred - y[test_idx]) ** 2))
        if not np.isnan(a):
            aurocs.append(a)
            briers.append(b)
    if not aurocs:
        return {"auroc": float("nan"), "brier": float("nan"), "k_folds": k_folds}
    return {
        "auroc_mean": round(float(np.mean(aurocs)), 4),
        "auroc_std": round(float(np.std(aurocs, ddof=1)) if len(aurocs) > 1 else 0.0, 4),
        "brier_mean": round(float(np.mean(briers)), 4),
        "brier_std": round(float(np.std(briers, ddof=1)) if len(briers) > 1 else 0.0, 4),
        "k_folds": int(k_folds),
        "n_used": int(sum(len(folds[f]) for f in range(k_folds))),
    }


# ----------------------------------------------------------------------
# Score atual vs calibrado: comparacao por amostra
# ----------------------------------------------------------------------

def score_atual(X: np.ndarray) -> np.ndarray:
    w = np.array([CURRENT_WEIGHTS[d] for d in DIMS])
    return X @ w  # 0..100


def score_calibrado(X: np.ndarray, weights: dict[str, float]) -> np.ndarray:
    w = np.array([weights[d] for d in DIMS])
    return X @ w


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def run(
    db_path: str,
    simulate_n: int | None,
    output: str | None,
    show_diagram: bool,
) -> dict[str, Any]:
    if simulate_n is not None and simulate_n > 0:
        logger.info("Modo SIMULATE: gerando %d amostras sinteticas", simulate_n)
        X, k, n, domains = simulate_dataset(simulate_n)
        source = f"simulated_n{simulate_n}"
    else:
        logger.info("Carregando dataset real de %s", db_path)
        X, k, n, domains = load_dataset_from_db(db_path)
        source = f"db:{db_path}"
        if X.shape[0] == 0:
            logger.warning(
                "score_calibration_inputs vazia. "
                "Use --simulate N para um demo end-to-end."
            )
            return {"status": "empty", "source": source}

    logger.info("Dataset: %d sites, %d dimensoes", X.shape[0], X.shape[1])
    logger.info("Soma de queries: n=%d, k_cited=%d, taxa media=%.3f",
                int(n.sum()), int(k.sum()), float((k / np.maximum(n, 1)).mean()))

    # Expansao para Bernoulli
    X_b, y_b = expand_to_bernoulli(X, k, n)
    logger.info("Expandido para %d eventos Bernoulli", len(y_b))

    # Fit
    fit = fit_logit(X_b, y_b)
    if not fit.get("converged"):
        logger.error("Logit nao convergiu: %s", fit.get("error"))
        return {"status": "fit_failed", "error": fit.get("error"), "source": source}

    coefs = fit["coefficients"]
    weights_calibrated = compute_calibrated_weights(coefs)

    # CV
    cv = cv_auroc(X_b, y_b, k_folds=5)

    # Metricas in-sample
    sa = StatisticalAnalyzer()
    p_pred = fit["_model_obj"].predict()
    brier = sa.brier_score(p_pred.tolist(), y_b.tolist())
    diagram = sa.reliability_diagram(p_pred.tolist(), y_b.tolist(), n_bins=10)

    # Limpa o objeto modelo antes do dump
    del fit["_model_obj"]

    # Comparacao Score atual vs calibrado (por site)
    sc_atual = score_atual(X)
    sc_calib = score_calibrado(X, weights_calibrated)
    cmp = {
        "score_current_mean": round(float(sc_atual.mean()), 2),
        "score_calibrated_mean": round(float(sc_calib.mean()), 2),
        "score_correlation_spearman": round(
            float(__import__("scipy.stats", fromlist=["spearmanr"]).spearmanr(sc_atual, sc_calib).statistic),
            4,
        ),
    }

    result = {
        "status": "ok",
        "source": source,
        "n_sites": int(X.shape[0]),
        "n_bernoulli_events": int(len(y_b)),
        "current_weights": CURRENT_WEIGHTS,
        "calibrated_weights": weights_calibrated,
        "weight_delta": {
            d: round(weights_calibrated[d] - CURRENT_WEIGHTS[d], 2)
            for d in DIMS
        },
        "fit": fit,
        "cross_validation": cv,
        "in_sample_calibration": brier,
        "reliability_diagram": diagram,
        "score_comparison": cmp,
    }

    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        logger.info("Resultado salvo em %s", output)

    if show_diagram:
        print("\n=== Reliability diagram (predicted_mean -> observed_mean, n) ===")
        for b in diagram:
            print(f"  [{b['bin_lo']:.1f}, {b['bin_hi']:.1f}]  pred={b['predicted_mean']:.3f}  obs={b['observed_mean']:.3f}  n={b['n']}")

    return result


def _parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", default=DB_PATH, help=f"Caminho do SQLite (default: {DB_PATH})")
    p.add_argument("--simulate", type=int, default=None, metavar="N",
                   help="Gera dataset sintetico de N sites (ignora o DB)")
    p.add_argument("--output", default=None, metavar="PATH",
                   help="Salva resultado em JSON")
    p.add_argument("--diagram", action="store_true", help="Imprime reliability diagram")
    return p.parse_args()


def main() -> int:
    args = _parse()
    result = run(args.db, args.simulate, args.output, args.diagram)
    print()
    print("=" * 70)
    if result.get("status") != "ok":
        print(f"STATUS: {result.get('status')}  source={result.get('source')}")
        return 1
    print(f"STATUS: ok    source={result['source']}")
    print(f"sites={result['n_sites']}  bernoulli={result['n_bernoulli_events']}")
    print()
    print("Pesos (atual -> calibrado, delta):")
    for d in DIMS:
        cur = result["current_weights"][d]
        cal = result["calibrated_weights"][d]
        delta = result["weight_delta"][d]
        sign = "+" if delta >= 0 else ""
        print(f"  {d:32s}  {cur:5.1f} -> {cal:5.1f}  ({sign}{delta:.1f})")
    print()
    fit = result["fit"]
    print(f"pseudo R2 (McFadden): {fit['pseudo_r2_mcfadden']:.4f}")
    print(f"AIC: {fit['aic']:.1f}   BIC: {fit['bic']:.1f}")
    cv = result["cross_validation"]
    if "auroc_mean" in cv:
        print(f"5-fold CV AUROC: {cv['auroc_mean']:.4f} (+/- {cv['auroc_std']:.4f})")
        print(f"5-fold CV Brier: {cv['brier_mean']:.4f} (+/- {cv['brier_std']:.4f})")
    print(f"In-sample Brier: {result['in_sample_calibration']['brier_score']:.4f}")
    cmp = result["score_comparison"]
    print(f"Spearman(score_atual, score_calibrado): {cmp['score_correlation_spearman']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
