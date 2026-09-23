"""
feature_engineering.py
-----------------------
Reusable feature-engineering functions for the AI MarketLens project.

All functions accept a DataFrame and return a new DataFrame with
additional columns; original columns are never dropped here unless
explicitly requested.

Leakage warnings are documented per function.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Salary features
# ---------------------------------------------------------------------------

def add_salary_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add salary_mid and salary_range if not already present.

    salary_mid   = (salary_min_usd + salary_max_usd) / 2
    salary_range = salary_max_usd - salary_min_usd
    """
    df = df.copy()
    if "salary_mid" not in df.columns:
        df["salary_mid"]   = (df["salary_min_usd"] + df["salary_max_usd"]) / 2
    if "salary_range" not in df.columns:
        df["salary_range"] = df["salary_max_usd"] - df["salary_min_usd"]
    return df


# ---------------------------------------------------------------------------
# Experience features
# ---------------------------------------------------------------------------

def add_experience_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add experience_numeric: a clean integer encoding of experience_level.

    Mapping: Entry -> 0, Mid -> 1, Senior -> 2

    NOTE: min_experience_years (values 0/2/5) encodes the same information.
    Do NOT use both experience_numeric and min_experience_years as features
    in the same ML model — that is redundancy / leakage.
    """
    df = df.copy()
    mapping = {"Entry": 0, "Mid": 1, "Senior": 2}
    df["experience_numeric"] = df["experience_level"].map(mapping)
    return df


# ---------------------------------------------------------------------------
# Time features
# ---------------------------------------------------------------------------

def add_period_type(df: pd.DataFrame,
                    year_col: str = "posted_year") -> pd.DataFrame:
    """
    Add period_type: 'Historical' (2020–2024) or 'Projected' (2025–2026).

    Projected rows must be clearly separated in temporal analyses to avoid
    treating synthetic forward-looking data as historical observations.
    """
    df = df.copy()
    df["period_type"] = np.where(df[year_col] <= 2024, "Historical", "Projected")
    return df


def add_year_group(df: pd.DataFrame,
                   year_col: str = "posted_year") -> pd.DataFrame:
    """
    Add year_group: groups years into early/mid/late bands.

    2020-2021 -> 'Early'
    2022-2023 -> 'Mid'
    2024-2026 -> 'Late'
    """
    df = df.copy()
    bins   = [2019, 2021, 2023, 2026]
    labels = ["Early (2020–21)", "Mid (2022–23)", "Late (2024–26)"]
    df["year_group"] = pd.cut(df[year_col], bins=bins, labels=labels)
    return df


# ---------------------------------------------------------------------------
# Remote / work-mode features
# ---------------------------------------------------------------------------

def add_remote_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add remote_flag: 1 if remote_type == 'Remote', else 0.

    NOTE: city == 'Remote' is a perfect predictor of remote_flag == 1.
    Exclude 'city' when using remote_flag as an ML target to avoid leakage.
    """
    df = df.copy()
    df["remote_flag"] = (df["remote_type"] == "Remote").astype(int)
    return df


# ---------------------------------------------------------------------------
# Company features
# ---------------------------------------------------------------------------

def add_company_size_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add company_size_numeric: ordinal encoding of company_size.

    Small -> 1, Medium -> 2, Large -> 3
    """
    df = df.copy()
    mapping = {"Small": 1, "Medium": 2, "Large": 3}
    df["company_size_numeric"] = df["company_size"].map(mapping)
    return df


# ---------------------------------------------------------------------------
# One-hot / label encoding helpers
# ---------------------------------------------------------------------------

CATEGORICAL_COLS_FOR_ML = [
    "job_title",
    "company_type",
    "industry",
    "country",
    "remote_type",
    "experience_level",
    "company_size",
    "role_category",
]


def encode_categoricals(df: pd.DataFrame,
                         columns: list = None,
                         drop_first: bool = True) -> pd.DataFrame:
    """
    One-hot encode categorical columns for ML.

    Parameters
    ----------
    df       : DataFrame containing the columns to encode
    columns  : list of column names to encode; defaults to CATEGORICAL_COLS_FOR_ML
    drop_first : drop the first dummy column to avoid multicollinearity

    Returns
    -------
    DataFrame with original categorical columns replaced by dummies.
    """
    if columns is None:
        columns = [c for c in CATEGORICAL_COLS_FOR_ML if c in df.columns]
    df = pd.get_dummies(df, columns=columns, drop_first=drop_first)
    return df


# ---------------------------------------------------------------------------
# ML feature set builder
# ---------------------------------------------------------------------------

# Columns to ALWAYS exclude from ML features
LEAKAGE_COLUMNS = [
    "job_id",          # identifier
    "city",            # leaks remote_type (city='Remote' -> remote_type='Remote')
    "employment_type", # zero-variance (all Full-time) — should already be dropped
]

REDUNDANT_COLUMNS = [
    # When experience_level is included, drop min_experience_years (same info)
    "min_experience_years",
]


def build_ml_feature_matrix(df: pd.DataFrame,
                              target: str,
                              exclude_leakage: bool = True,
                              exclude_redundant: bool = True,
                              encode: bool = True) -> tuple:
    """
    Build a clean (X, y) pair for ML experiments.

    Parameters
    ----------
    df               : cleaned jobs DataFrame (output of preprocessing pipeline)
    target           : name of the target column
    exclude_leakage  : if True, drop known leakage columns
    exclude_redundant: if True, drop columns redundant with the target
    encode           : if True, one-hot encode categoricals

    Returns
    -------
    X : pd.DataFrame — feature matrix
    y : pd.Series    — target vector
    feature_names : list of str
    """
    drop_cols = [target]

    if exclude_leakage:
        drop_cols += [c for c in LEAKAGE_COLUMNS if c in df.columns]

    if exclude_redundant:
        # If target is salary_mid, drop salary_min_usd / salary_max_usd / salary_range
        if target in ("salary_mid", "salary_min_usd", "salary_max_usd"):
            for c in ["salary_min_usd", "salary_max_usd", "salary_range",
                      "salary_mid"]:
                if c != target and c in df.columns:
                    drop_cols.append(c)
        # Drop experience_numeric if experience_level is present (or vice-versa)
        if "experience_level" in df.columns and "experience_numeric" in df.columns:
            drop_cols.append("experience_numeric")
        # Always drop min_experience_years when experience_level is present
        if "experience_level" in df.columns:
            drop_cols.append("min_experience_years")

    # Drop period_type if not useful for the specific target
    non_feature_cols = ["period_type", "year_group", "posted_year"]
    # Keep posted_year as a feature — useful for trend
    # Drop year_group if period_type already encoded
    if "period_type" in df.columns and "year_group" in df.columns:
        drop_cols.append("year_group")

    drop_cols = list(set(c for c in drop_cols if c in df.columns))

    X = df.drop(columns=drop_cols)
    y = df[target]

    if encode:
        cat_cols = [c for c in CATEGORICAL_COLS_FOR_ML if c in X.columns]
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    # Drop any remaining non-numeric columns that slipped through
    X = X.select_dtypes(include=[np.number, "bool"])

    return X, y, list(X.columns)


# ---------------------------------------------------------------------------
# Apply all standard feature engineering at once
# ---------------------------------------------------------------------------

def engineer_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the full suite of feature-engineering steps to the cleaned jobs
    DataFrame and return the enriched DataFrame.
    """
    df = add_salary_features(df)
    df = add_experience_numeric(df)
    df = add_period_type(df)
    df = add_year_group(df)
    df = add_remote_flag(df)
    df = add_company_size_numeric(df)
    return df
