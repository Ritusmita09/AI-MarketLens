"""
utils.py
--------
Shared utility helpers for the AI MarketLens project.

Covers: plotting defaults, display helpers, statistical test wrappers,
        and report-writing helpers.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------

_SRC_DIR     = Path(__file__).resolve().parent
PROJECT_ROOT = _SRC_DIR.parent
REPORTS_DIR  = PROJECT_ROOT / "reports"

# ---------------------------------------------------------------------------
# Plot style defaults
# ---------------------------------------------------------------------------

PALETTE_MAIN   = "Blues_d"
PALETTE_QUAL   = "tab10"
COLOR_HIST     = "#3b82d4"   # historical accent
COLOR_PROJ     = "#f59e0b"   # projected accent (amber)
COLOR_NEUTRAL  = "#57606a"

FIGSIZE_WIDE   = (12, 5)
FIGSIZE_SQUARE = (8, 6)
FIGSIZE_TALL   = (10, 8)

DPI = 120


def set_plot_style() -> None:
    """Apply consistent matplotlib / seaborn style."""
    sns.set_theme(style="whitegrid", palette=PALETTE_QUAL)
    plt.rcParams.update({
        "figure.dpi":        DPI,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "font.size":         11,
        "axes.titlesize":    13,
        "axes.labelsize":    11,
        "legend.fontsize":   10,
    })


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_section(title: str, width: int = 60) -> None:
    """Print a bold section header to stdout."""
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def df_summary(df: pd.DataFrame, name: str = "") -> None:
    """Quick DataFrame summary to stdout."""
    tag = f" [{name}]" if name else ""
    print(f"\nDataFrame{tag}: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Missing values : {df.isnull().sum().sum()}")
    print(f"  Duplicates     : {df.duplicated().sum()}")
    print(f"  dtypes         : {dict(df.dtypes.value_counts())}")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_usd(value: float) -> str:
    """Format a number as USD with comma thousands separator."""
    return f"${value:,.0f}"


def fmt_pct(value: float) -> str:
    """Format a number as a percentage string."""
    return f"{value:.1f}%"


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------

def run_anova(df: pd.DataFrame,
              group_col: str,
              value_col: str,
              alpha: float = 0.05) -> dict:
    """
    One-way ANOVA: tests whether the means of value_col differ across groups
    defined by group_col.

    Null hypothesis (H0): all group means are equal.
    Alternative  (H1)   : at least one group mean differs.

    Parameters
    ----------
    df        : DataFrame
    group_col : categorical grouping column
    value_col : numeric column
    alpha     : significance level (default 0.05)

    Returns
    -------
    dict with keys: groups, F, p_value, significant, interpretation
    """
    from scipy import stats

    groups = [grp[value_col].dropna().values
              for _, grp in df.groupby(group_col)]
    F, p = stats.f_oneway(*groups)

    result = {
        "test":          "One-way ANOVA",
        "H0":            f"Mean {value_col} is equal across all {group_col} groups",
        "H1":            f"At least one {group_col} group has a different mean {value_col}",
        "groups":        df[group_col].nunique(),
        "F_statistic":   round(float(F), 4),
        "p_value":       round(float(p), 6),
        "alpha":         alpha,
        "significant":   bool(p < alpha),
        "interpretation": (
            f"p={p:.4f} < {alpha} → Reject H0. Significant difference in "
            f"{value_col} across {group_col} groups."
            if p < alpha else
            f"p={p:.4f} ≥ {alpha} → Fail to reject H0. No significant "
            f"difference detected."
        ),
    }
    return result


def run_kruskal(df: pd.DataFrame,
                group_col: str,
                value_col: str,
                alpha: float = 0.05) -> dict:
    """
    Kruskal-Wallis H-test: non-parametric alternative to one-way ANOVA.
    Does not assume normality.

    Parameters and return format same as run_anova().
    """
    from scipy import stats

    groups = [grp[value_col].dropna().values
              for _, grp in df.groupby(group_col)]
    H, p = stats.kruskal(*groups)

    result = {
        "test":          "Kruskal-Wallis H-test",
        "H0":            f"Distribution of {value_col} is equal across all {group_col} groups",
        "H1":            f"At least one {group_col} group has a different distribution of {value_col}",
        "groups":        df[group_col].nunique(),
        "H_statistic":   round(float(H), 4),
        "p_value":       round(float(p), 6),
        "alpha":         alpha,
        "significant":   bool(p < alpha),
        "interpretation": (
            f"p={p:.4f} < {alpha} → Reject H0. Significant difference in "
            f"{value_col} distributions across {group_col} groups."
            if p < alpha else
            f"p={p:.4f} ≥ {alpha} → Fail to reject H0. No significant "
            f"difference detected."
        ),
    }
    return result


def print_test_result(result: dict) -> None:
    """Pretty-print a statistical test result dict."""
    print(f"\n  Test      : {result['test']}")
    print(f"  H0        : {result['H0']}")
    print(f"  H1        : {result['H1']}")
    stat_key = "F_statistic" if "F_statistic" in result else "H_statistic"
    print(f"  Statistic : {result[stat_key]}")
    print(f"  p-value   : {result['p_value']}")
    print(f"  α         : {result['alpha']}")
    print(f"  Result    : {'⚠ SIGNIFICANT' if result['significant'] else 'NOT significant'}")
    print(f"  Interp.   : {result['interpretation']}")


# ---------------------------------------------------------------------------
# ML metric helpers
# ---------------------------------------------------------------------------

def regression_metrics(y_true, y_pred, label: str = "") -> dict:
    """
    Compute MAE, RMSE, and R² for a regression model.

    Returns a dict and prints results to stdout.
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)

    metrics = {
        "label": label,
        "MAE":   round(mae,  2),
        "RMSE":  round(rmse, 2),
        "R2":    round(r2,   4),
    }

    tag = f"  [{label}]" if label else ""
    print(f"\n  Regression Metrics{tag}")
    print(f"    MAE  : {fmt_usd(mae)}")
    print(f"    RMSE : {fmt_usd(rmse)}")
    print(f"    R²   : {r2:.4f}")
    return metrics


# ---------------------------------------------------------------------------
# Cluster evaluation helper
# ---------------------------------------------------------------------------

def cluster_evaluation_report(X_scaled, labels) -> dict:
    """
    Compute Silhouette Score and Davies-Bouldin Index for a clustering result.

    Parameters
    ----------
    X_scaled : array-like, scaled feature matrix
    labels   : cluster label array

    Returns dict with silhouette and davies_bouldin scores.
    """
    from sklearn.metrics import silhouette_score, davies_bouldin_score

    sil = silhouette_score(X_scaled, labels)
    dbi = davies_bouldin_score(X_scaled, labels)

    print(f"\n  Clustering Evaluation")
    print(f"    Silhouette Score    : {sil:.4f}  (higher is better, range −1 to 1)")
    print(f"    Davies-Bouldin Index: {dbi:.4f}  (lower is better)")
    return {"silhouette": round(sil, 4), "davies_bouldin": round(dbi, 4)}


# ---------------------------------------------------------------------------
# Save figure helper
# ---------------------------------------------------------------------------

def save_figure(fig: plt.Figure, filename: str,
                subdir: str = "figures") -> Path:
    """
    Save a matplotlib figure to reports/<subdir>/<filename>.

    Returns the saved path.
    """
    out_dir = REPORTS_DIR / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    fig.savefig(path, bbox_inches="tight", dpi=DPI)
    return path
