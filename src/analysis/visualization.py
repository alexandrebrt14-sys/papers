"""Publication-quality visualization for GEO research data."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Publication style
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.figsize": (10, 6),
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.family": "sans-serif",
})

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def plot_citation_rate_by_llm(
    data: pd.DataFrame, output: str = "citation_rate_by_llm.png",
) -> str:
    """Bar chart: citation rate per LLM with confidence intervals."""
    fig, ax = plt.subplots()

    rates = data.groupby("llm")["cited"].agg(["mean", "sem", "count"])
    rates = rates.sort_values("mean", ascending=True)

    colors = sns.color_palette("viridis", len(rates))
    bars = ax.barh(
        rates.index, rates["mean"], xerr=rates["sem"] * 1.96,
        color=colors, edgecolor="white", linewidth=0.5,
    )
    ax.set_xlabel("Taxa de Citação")
    ax.set_title("Taxa de Citação por LLM (IC 95%)")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))

    for bar, (_, row) in zip(bars, rates.iterrows()):
        ax.text(
            bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
            f"n={int(row['count'])}", va="center", fontsize=9,
        )

    path = str(OUTPUT_DIR / output)
    fig.savefig(path)
    plt.close(fig)
    logger.info(f"Gráfico salvo: {path}")
    return path


def plot_citation_trend(
    data: pd.DataFrame, output: str = "citation_trend.png",
) -> str:
    """Line chart: citation rate over time by LLM."""
    fig, ax = plt.subplots()

    data["date"] = pd.to_datetime(data["timestamp"]).dt.date
    daily = data.groupby(["date", "llm"])["cited"].mean().reset_index()

    for llm in daily["llm"].unique():
        subset = daily[daily["llm"] == llm]
        ax.plot(subset["date"], subset["cited"], marker="o", markersize=3, label=llm)

    ax.set_xlabel("Data")
    ax.set_ylabel("Taxa de Citação")
    ax.set_title("Evolução da Taxa de Citação por LLM")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.legend(loc="best")
    fig.autofmt_xdate()

    path = str(OUTPUT_DIR / output)
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_serp_ai_overlap(
    data: pd.DataFrame, output: str = "serp_ai_overlap.png",
) -> str:
    """Grouped bar chart: SERP vs AI overlap by LLM."""
    fig, ax = plt.subplots()

    agg = data.groupby("llm")["overlap_pct"].agg(["mean", "sem"]).sort_values("mean")

    bars = ax.barh(
        agg.index, agg["mean"], xerr=agg["sem"] * 1.96,
        color=sns.color_palette("rocket", len(agg)), edgecolor="white",
    )
    ax.set_xlabel("Sobreposição SERP-IA (%)")
    ax.set_title("Sobreposição entre Google SERP e Respostas de IA")

    path = str(OUTPUT_DIR / output)
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_competitor_comparison(
    data: pd.DataFrame, output: str = "competitor_comparison.png",
) -> str:
    """Heatmap: citation rate per entity x LLM."""
    fig, ax = plt.subplots(figsize=(12, 6))

    pivot = data.pivot_table(
        values="cited", index="entity", columns="llm", aggfunc="mean",
    )
    sns.heatmap(
        pivot, annot=True, fmt=".0%", cmap="YlGnBu",
        ax=ax, linewidths=0.5, vmin=0, vmax=1,
    )
    ax.set_title("Taxa de Citação: Entidade vs LLM")

    path = str(OUTPUT_DIR / output)
    fig.savefig(path)
    plt.close(fig)
    return path


def plot_intervention_impact(
    measurements: list[dict[str, Any]], baseline_rate: float,
    output: str = "intervention_impact.png",
) -> str:
    """Line chart: citation rate before/after intervention."""
    fig, ax = plt.subplots()

    days = [m["days_since_intervention"] for m in measurements]
    rates = [m["citation_rate"] for m in measurements]

    ax.axhline(y=baseline_rate, color="gray", linestyle="--", label="Baseline")
    ax.axvline(x=0, color="red", linestyle=":", alpha=0.5, label="Intervenção")
    ax.plot(days, rates, marker="o", color="#0176d3", linewidth=2, label="Pós-intervenção")

    ax.set_xlabel("Dias desde a Intervenção")
    ax.set_ylabel("Taxa de Citação")
    ax.set_title("Impacto da Intervenção na Taxa de Citação")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.legend()

    path = str(OUTPUT_DIR / output)
    fig.savefig(path)
    plt.close(fig)
    return path
