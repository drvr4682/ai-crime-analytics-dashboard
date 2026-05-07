"""
analysis.py
===========
Generates all 5 charts and saves them to static/graphs/.
Each function saves one PNG and returns the filename.
"""

import os
import matplotlib
matplotlib.use("Agg")          # Non-interactive backend – required for Flask
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

# ── Shared style ───────────────────────────────────────────────────────────────
DARK_BG   = "#0d1117"
CARD_BG   = "#161b22"
ACCENT    = "#00d4aa"
ACCENT2   = "#ff6b6b"
TEXT      = "#e6edf3"
GRID      = "#21262d"
PALETTE   = ["#00d4aa", "#ff6b6b", "#ffd166", "#a8dadc", "#c77dff",
             "#06d6a0", "#ef476f", "#118ab2", "#ffd60a", "#8ecae6"]

def _apply_dark_style(fig, ax):
    """Applies the shared dark theme to a matplotlib figure/axes."""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(ACCENT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
    ax.grid(axis="y", color=GRID, linestyle="--", linewidth=0.6, alpha=0.7)


def _save(fig, graphs_dir, filename):
    """Saves figure to disk and closes it."""
    os.makedirs(graphs_dir, exist_ok=True)
    path = os.path.join(graphs_dir, filename)
    fig.savefig(path, bbox_inches="tight", dpi=130, facecolor=DARK_BG)
    plt.close(fig)
    return filename


# ── 1. Bar Chart – Top 10 Cities by Crime Count ───────────────────────────────
def bar_chart(df: pd.DataFrame, graphs_dir: str) -> str:
    """
    Shows the 10 cities that reported the most crimes.
    Useful for identifying high-crime urban areas.
    """
    col = next((c for c in df.columns if "city" in c.lower()), None)
    if col is None:
        return None

    counts = df[col].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(counts.index, counts.values, color=PALETTE[:len(counts)],
                  edgecolor="none", width=0.6)
    ax.bar_label(bars, padding=3, color=TEXT, fontsize=8)
    ax.set_title("Top 10 Cities by Crime Count", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlabel("City", fontsize=10)
    ax.set_ylabel("Number of Cases", fontsize=10)
    plt.xticks(rotation=35, ha="right")
    _apply_dark_style(fig, ax)
    return _save(fig, graphs_dir, "bar_chart.png")


# ── 2. Pie Chart – Crime Domain Distribution ──────────────────────────────────
def pie_chart(df: pd.DataFrame, graphs_dir: str) -> str:
    """
    Shows the proportional share of each crime category/domain.
    Helps understand which crime type is most prevalent.
    """
    col = next((c for c in df.columns
                if any(k in c.lower() for k in ["domain", "type", "description"])), None)
    if col is None:
        return None

    counts = df[col].value_counts().head(8)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(DARK_BG)
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=PALETTE[:len(counts)],
        startangle=140,
        pctdistance=0.82,
        wedgeprops=dict(edgecolor=DARK_BG, linewidth=2),
    )
    for t in texts:
        t.set_color(TEXT); t.set_fontsize(9)
    for at in autotexts:
        at.set_color(DARK_BG); at.set_fontsize(8); at.set_fontweight("bold")
    ax.set_title("Crime Domain Distribution", fontsize=14, fontweight="bold",
                 color=ACCENT, pad=16)
    return _save(fig, graphs_dir, "pie_chart.png")


# ── 3. Heatmap – Crime Frequency by Month and City (top 8) ────────────────────
def heatmap(df: pd.DataFrame, graphs_dir: str) -> str:
    """
    A correlation/frequency heatmap:
    rows = months, columns = top cities.
    Reveals seasonal crime spikes in specific cities.
    """
    if "Month" not in df.columns:
        return None
    city_col = next((c for c in df.columns if "city" in c.lower()), None)
    if city_col is None:
        return None

    top_cities = df[city_col].value_counts().head(8).index
    sub = df[df[city_col].isin(top_cities)]
    pivot = sub.groupby(["Month", city_col]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    sns.heatmap(
        pivot, ax=ax, cmap="YlOrRd", linewidths=0.4,
        linecolor=DARK_BG, annot=True, fmt="d",
        annot_kws={"size": 8, "color": DARK_BG},
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("Monthly Crime Frequency by City", fontsize=14,
                 fontweight="bold", color=ACCENT, pad=14)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.set_xlabel("City", fontsize=10, color=TEXT)
    ax.set_ylabel("Month", fontsize=10, color=TEXT)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", color=TEXT)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color=TEXT)
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors=TEXT)
    return _save(fig, graphs_dir, "heatmap.png")


# ── 4. Line Chart – Crimes per Year ───────────────────────────────────────────
def line_chart(df: pd.DataFrame, graphs_dir: str) -> str:
    """
    Plots the total number of crimes recorded each year.
    Highlights whether crime is increasing or decreasing over time.
    """
    if "Year" not in df.columns:
        return None

    yearly = df[df["Year"] > 0].groupby("Year").size()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(yearly.index, yearly.values, color=ACCENT, linewidth=2.5,
            marker="o", markersize=6, markerfacecolor=ACCENT2)
    ax.fill_between(yearly.index, yearly.values, alpha=0.15, color=ACCENT)
    ax.set_title("Crime Trend Over the Years", fontsize=14,
                 fontweight="bold", pad=14)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Number of Cases", fontsize=10)
    _apply_dark_style(fig, ax)
    return _save(fig, graphs_dir, "line_chart.png")


# ── 5. Scatter Plot – Victim Age vs Police Deployed ───────────────────────────
def scatter_plot(df: pd.DataFrame, graphs_dir: str) -> str:
    """
    Scatter plot of Victim Age (x) vs Police Deployed (y).
    Colour-coded by Crime Domain.
    Reveals whether older victims receive more police resources.
    """
    age_col    = next((c for c in df.columns if "age"      in c.lower()), None)
    police_col = next((c for c in df.columns if "police"   in c.lower()), None)
    domain_col = next((c for c in df.columns if "domain"   in c.lower()), None)

    if age_col is None or police_col is None:
        return None

    sample = df[[age_col, police_col] + ([domain_col] if domain_col else [])].dropna()
    sample = sample.sample(min(3000, len(sample)), random_state=42)

    fig, ax = plt.subplots(figsize=(10, 6))
    if domain_col:
        domains = sample[domain_col].unique()
        for i, dom in enumerate(domains):
            mask = sample[domain_col] == dom
            ax.scatter(sample.loc[mask, age_col], sample.loc[mask, police_col],
                       color=PALETTE[i % len(PALETTE)], alpha=0.55,
                       s=20, label=dom)
        ax.legend(fontsize=8, facecolor=CARD_BG, labelcolor=TEXT,
                  framealpha=0.9, edgecolor=GRID)
    else:
        ax.scatter(sample[age_col], sample[police_col],
                   color=ACCENT, alpha=0.4, s=20)

    ax.set_title("Victim Age vs Police Deployed", fontsize=14,
                 fontweight="bold", pad=14)
    ax.set_xlabel("Victim Age", fontsize=10)
    ax.set_ylabel("Police Deployed", fontsize=10)
    _apply_dark_style(fig, ax)
    return _save(fig, graphs_dir, "scatter_plot.png")


# ── Master runner ─────────────────────────────────────────────────────────────
def generate_all(df: pd.DataFrame, graphs_dir: str) -> dict:
    """Runs all chart functions and returns a dict of {name: filename}."""
    return {
        "bar":     bar_chart(df, graphs_dir),
        "pie":     pie_chart(df, graphs_dir),
        "heatmap": heatmap(df, graphs_dir),
        "line":    line_chart(df, graphs_dir),
        "scatter": scatter_plot(df, graphs_dir),
    }