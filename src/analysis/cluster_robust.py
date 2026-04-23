"""cluster_robust.py — Cluster-robust standard errors CR1 para o paper 4 v2.

Resolve o gap A1 do Agent A audit (2026-04-23):

O `paper4_tables.py` atual usa `sqrt(se_a² + se_b²)` para cluster-robust SE
da diferença de proporções entre grupos (RAG vs parametric). Isso trata os
clusters (dias de coleta) como independentes POR grupo — mas os dias são
os MESMOS clusters em ambos os grupos (RAG e parametric rodam no mesmo dia).
Violação de independência entre-grupo → subestima inflation factor.

Correção: estimador sanduíche CR1 com scores pooled por dia, considerando
a covariância cruzada entre RAG e parametric no mesmo dia.

Referência: Cameron, Gelbach, Miller (2011) "Robust Inference With
Multiway Clustering"; MacKinnon, Webb (2017) "Wild Bootstrap Inference
for Wildly Different Cluster Sizes".

Uso:
    from src.analysis.cluster_robust import cluster_robust_diff_proportions

    result = cluster_robust_diff_proportions(
        cited_a=df["cited"][df["is_rag"]],
        cited_b=df["cited"][~df["is_rag"]],
        cluster_a=df["day"][df["is_rag"]],
        cluster_b=df["day"][~df["is_rag"]],
    )
    # → {"diff": -0.0258, "se_iid": 0.01449, "se_cluster": 0.02336,
    #    "inflation": 1.61, "ci_low": -0.07, "ci_high": 0.02,
    #    "p_value": 0.48, "t_stat": -1.10, "df": 11}
"""
from __future__ import annotations

import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class ClusterRobustResult:
    """Resultado do estimador CR1 sandwich para diferença de proporções."""
    diff: float           # p_a - p_b (estimativa pontual)
    n_a: int
    n_b: int
    n_clusters: int       # Número de dias/clusters únicos
    se_iid: float         # SE iid naive (sqrt(pa(1-pa)/na + pb(1-pb)/nb))
    se_cluster: float     # SE cluster-robust CR1 com cross-group covariance
    inflation: float      # se_cluster / se_iid
    t_stat: float         # diff / se_cluster
    p_value: float        # two-sided, t(G-1)
    df: int               # G-1 graus de liberdade
    ci_low: float         # t(G-1) 0.025 critical value
    ci_high: float

    def to_dict(self) -> dict:
        return asdict(self)


def cluster_robust_diff_proportions(
    cited_a: np.ndarray,
    cited_b: np.ndarray,
    cluster_a: np.ndarray,
    cluster_b: np.ndarray,
) -> ClusterRobustResult:
    """Estimador CR1 para diferença de proporções entre dois grupos A e B
    quando ambos compartilham clusters temporais.

    Args:
        cited_a, cited_b: arrays 0/1 indicando cited=True por observação
        cluster_a, cluster_b: labels de cluster (dia) para cada observação

    Returns:
        ClusterRobustResult com diff, SEs, inflation, p-value, CI.

    Mecânica:
        Seja Y_ag = 1{resposta g do grupo A citou} e Y_bg idem. Para cada
        cluster c (dia), computa scores agregados:
            ψ_c^A = Σ_{g ∈ c, a} (Y_ag - p_a)
            ψ_c^B = Σ_{g ∈ c, b} (Y_bg - p_b)
        Variância cluster-robust CR1 da diferença:
            V(diff) = (G/(G-1)) · Σ_c (ψ_c^A/n_a - ψ_c^B/n_b)^2
        onde G é o número de clusters distintos (união de A e B).

        O cross-group term é crítico: quando dias "ruins" (e.g. rate global
        baixo) afetam AMBOS os grupos, a covariância é POSITIVA, o que
        REDUZ a variância da DIFERENÇA (termos se cancelam). Quando só
        um grupo tem dias ruins, covariância é pequena e variância da
        diferença é próxima à soma das variâncias por-grupo.

        Fórmula matricial equivalente (mais fácil de implementar):
            diff_g = (p̂_a na cluster g) - (p̂_b na cluster g), ponderado
            pelas participações n_{a,g}/n_a e n_{b,g}/n_b.
    """
    cited_a = np.asarray(cited_a, dtype=float)
    cited_b = np.asarray(cited_b, dtype=float)
    cluster_a = np.asarray(cluster_a)
    cluster_b = np.asarray(cluster_b)

    n_a, n_b = len(cited_a), len(cited_b)
    if n_a == 0 or n_b == 0:
        raise ValueError("Grupos vazios não permitidos")

    p_a = cited_a.mean()
    p_b = cited_b.mean()
    diff = p_a - p_b

    # SE iid (referência)
    se_iid = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)

    # Clusters únicos (união)
    all_clusters = np.unique(np.concatenate([cluster_a, cluster_b]))
    G = len(all_clusters)
    if G < 2:
        # Sem clusters suficientes; retorna iid como cluster
        return ClusterRobustResult(
            diff=diff, n_a=n_a, n_b=n_b, n_clusters=G,
            se_iid=se_iid, se_cluster=se_iid, inflation=1.0,
            t_stat=diff / se_iid if se_iid > 0 else float("nan"),
            p_value=_t_pvalue(diff / se_iid if se_iid > 0 else 0, df=max(1, G - 1)),
            df=max(1, G - 1),
            ci_low=diff - 1.96 * se_iid, ci_high=diff + 1.96 * se_iid,
        )

    # Score agregado por cluster, para diff = p_a - p_b
    # ψ_g = (1/n_a) Σ_{i in g, A} (y_i - p_a) - (1/n_b) Σ_{j in g, B} (y_j - p_b)
    scores = np.zeros(G)
    for k, c in enumerate(all_clusters):
        mask_a = cluster_a == c
        mask_b = cluster_b == c
        sum_a = (cited_a[mask_a] - p_a).sum() if mask_a.any() else 0.0
        sum_b = (cited_b[mask_b] - p_b).sum() if mask_b.any() else 0.0
        scores[k] = sum_a / n_a - sum_b / n_b

    # CR1: variância sanduíche com correção de graus de liberdade
    var_cluster = (G / (G - 1)) * np.sum(scores ** 2)
    se_cluster = np.sqrt(var_cluster)
    inflation = se_cluster / se_iid if se_iid > 0 else float("nan")

    # Teste t com G-1 graus de liberdade (não z — small G)
    df_t = G - 1
    t_stat = diff / se_cluster if se_cluster > 0 else float("nan")
    p_value = _t_pvalue(t_stat, df=df_t)

    # CI two-sided usando t-crit
    t_crit = _t_crit(alpha=0.05, df=df_t)
    ci_low = diff - t_crit * se_cluster
    ci_high = diff + t_crit * se_cluster

    return ClusterRobustResult(
        diff=diff, n_a=n_a, n_b=n_b, n_clusters=G,
        se_iid=se_iid, se_cluster=se_cluster, inflation=inflation,
        t_stat=t_stat, p_value=p_value, df=df_t,
        ci_low=ci_low, ci_high=ci_high,
    )


def _t_pvalue(t: float, df: int) -> float:
    """P-value two-sided de uma estatística t com df graus de liberdade."""
    try:
        from scipy import stats
        return float(2 * (1 - stats.t.cdf(abs(t), df)))
    except ImportError:
        # Fallback normal se scipy indisponível (só usar como last resort)
        import math
        return float(2 * (1 - _std_norm_cdf(abs(t))))


def _t_crit(alpha: float, df: int) -> float:
    """Critical value t two-sided para CI (1-alpha)."""
    try:
        from scipy import stats
        return float(stats.t.ppf(1 - alpha / 2, df))
    except ImportError:
        return 1.96  # approximation normal


def _std_norm_cdf(x: float) -> float:
    import math
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# ---------------------------------------------------------------------------
# Cluster-robust para rate global (sem grupo)
# ---------------------------------------------------------------------------

def cluster_robust_mean(
    values: np.ndarray,
    clusters: np.ndarray,
) -> dict:
    """SE cluster-robust para a média/taxa de uma série binária.

    Útil pra reportar CI do overall citation rate com correção por dia.
    Fórmula: V(p̂) = (G/(G-1)) · Σ_g (ȳ_g - p̂)^2 · (n_g/n)^2
    """
    values = np.asarray(values, dtype=float)
    clusters = np.asarray(clusters)
    n = len(values)
    p_hat = values.mean()

    unique_clusters = np.unique(clusters)
    G = len(unique_clusters)
    if G < 2:
        se_iid = np.sqrt(p_hat * (1 - p_hat) / max(1, n))
        return {"mean": p_hat, "n": n, "n_clusters": G,
                "se_iid": se_iid, "se_cluster": se_iid, "inflation": 1.0}

    var_cluster = 0.0
    for c in unique_clusters:
        mask = clusters == c
        n_g = int(mask.sum())
        if n_g == 0:
            continue
        y_g = values[mask].mean()
        var_cluster += (n_g / n) ** 2 * (y_g - p_hat) ** 2
    var_cluster *= G / (G - 1)

    se_cluster = np.sqrt(var_cluster)
    se_iid = np.sqrt(p_hat * (1 - p_hat) / n)
    return {
        "mean": p_hat, "n": n, "n_clusters": G,
        "se_iid": se_iid, "se_cluster": se_cluster,
        "inflation": se_cluster / se_iid if se_iid > 0 else float("nan"),
        "ci_low_cluster": p_hat - _t_crit(0.05, G - 1) * se_cluster,
        "ci_high_cluster": p_hat + _t_crit(0.05, G - 1) * se_cluster,
    }
