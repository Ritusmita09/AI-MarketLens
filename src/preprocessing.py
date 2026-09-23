"""
preprocessing.py
----------------
Cleaning, joining, and export functions for the AI MarketLens dataset.

Rules enforced here:
  - Raw files are never modified.
  - employment_type (zero-variance) is dropped.
  - The skills_demand <-> ai_jobs job_id join is KNOWN BROKEN (4.1% overlap).
    Skills are therefore processed independently; country-level skill
    aggregation uses country_ai_trends.top_skill only.
  - 2025-2026 rows are labelled "Projected"; 2020-2024 as "Historical".
  - All paths are resolved relative to the project root via pathlib.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

_SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SRC_DIR.parent

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
EXPORTS_DIR   = PROJECT_ROOT / "data" / "exports"


def _ensure_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# A. Clean Jobs Dataset
# ---------------------------------------------------------------------------

def clean_jobs(ai_jobs: pd.DataFrame, job_title_mapping: pd.DataFrame) -> pd.DataFrame:
    """
    Build the primary cleaned and feature-engineered jobs dataset.

    Steps:
      1. Drop employment_type (zero-variance: all rows are 'Full-time').
      2. Compute salary_mid and salary_range.
      3. Left-join role_category from job_title_mapping on job_title.
      4. Add period_type label (Historical / Projected).
      5. Enforce clean data types.

    Parameters
    ----------
    ai_jobs : raw ai_jobs DataFrame
    job_title_mapping : raw job_title_mapping DataFrame

    Returns
    -------
    pd.DataFrame — cleaned jobs dataset (50,000 rows expected)
    """
    df = ai_jobs.copy()

    # -- 1. Drop zero-variance column
    df = df.drop(columns=["employment_type"])

    # -- 2. Derived salary columns
    df["salary_mid"]   = (df["salary_min_usd"] + df["salary_max_usd"]) / 2
    df["salary_range"] = df["salary_max_usd"] - df["salary_min_usd"]

    # -- 3. Merge role_category from job_title_mapping
    role_map = job_title_mapping[["job_title", "role_category"]].copy()
    df = df.merge(role_map, on="job_title", how="left")

    # -- 4. Historical / Projected label
    df["period_type"] = np.where(df["posted_year"] <= 2024, "Historical", "Projected")

    # -- 5. Enforce types
    df["posted_year"]            = df["posted_year"].astype(int)
    df["min_experience_years"]   = df["min_experience_years"].astype(int)
    df["salary_min_usd"]         = df["salary_min_usd"].astype(int)
    df["salary_max_usd"]         = df["salary_max_usd"].astype(int)
    df["salary_mid"]             = df["salary_mid"].astype(float)
    df["salary_range"]           = df["salary_range"].astype(float)

    return df


# ---------------------------------------------------------------------------
# B. Country-Enriched Jobs Dataset
# ---------------------------------------------------------------------------

def build_country_enriched(jobs_clean: pd.DataFrame,
                            country_ai_trends: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join country_ai_trends onto the cleaned jobs dataset using
    (country, posted_year) == (country, year).

    Market-level columns are prefixed with 'market_' to distinguish them
    from job-level columns.

    Parameters
    ----------
    jobs_clean : output of clean_jobs()
    country_ai_trends : raw country_ai_trends DataFrame

    Returns
    -------
    pd.DataFrame — 50,000 rows expected (LEFT JOIN preserves all job rows)
    """
    # Rename country_ai_trends columns so they don't clash after the join
    trends = country_ai_trends.rename(columns={
        "year":               "posted_year",
        "total_ai_jobs":      "market_total_ai_jobs",
        "avg_salary_usd":     "market_avg_salary_usd",
        "remote_percentage":  "market_remote_percentage",
        "top_skill":          "market_top_skill",
    })

    enriched = jobs_clean.merge(
        trends[["country", "posted_year",
                "market_total_ai_jobs", "market_avg_salary_usd",
                "market_remote_percentage", "market_top_skill"]],
        on=["country", "posted_year"],
        how="left",
    )

    assert len(enriched) == len(jobs_clean), (
        f"Row count changed after enrichment join: "
        f"{len(jobs_clean)} -> {len(enriched)}"
    )
    assert enriched[["market_total_ai_jobs", "market_avg_salary_usd",
                      "market_remote_percentage", "market_top_skill"]].isnull().sum().sum() == 0, \
        "Unexpected NULLs after country enrichment join."

    return enriched


# ---------------------------------------------------------------------------
# C. Skills Processing (independent — no direct job_id join)
# ---------------------------------------------------------------------------

def clean_skills(skills_demand: pd.DataFrame) -> pd.DataFrame:
    """
    Return a lightly cleaned copy of skills_demand.

    NOTE: skills_demand.job_id does NOT reliably join to ai_jobs.job_id
    (only 4.1% overlap — dataset generation artifact).  This function
    processes skills independently.  The original job_id column is
    preserved for reference only.

    Parameters
    ----------
    skills_demand : raw skills_demand DataFrame

    Returns
    -------
    pd.DataFrame — 224,605 rows (no rows dropped)
    """
    df = skills_demand.copy()
    # Standardise string casing (already clean, but defensive)
    for col in ["skill", "skill_category", "skill_level"]:
        df[col] = df[col].str.strip()
    return df


def build_skill_summary(skills_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate skill frequency, category frequency, and level frequency
    into a single long-format summary DataFrame.

    Columns: summary_type, value, count, pct
    """
    frames = []

    # Skill frequency
    freq = skills_clean["skill"].value_counts().reset_index()
    freq.columns = ["value", "count"]
    freq["summary_type"] = "skill_frequency"
    freq["pct"] = (freq["count"] / len(skills_clean) * 100).round(2)
    frames.append(freq)

    # Skill category frequency
    cat_freq = skills_clean["skill_category"].value_counts().reset_index()
    cat_freq.columns = ["value", "count"]
    cat_freq["summary_type"] = "skill_category_frequency"
    cat_freq["pct"] = (cat_freq["count"] / len(skills_clean) * 100).round(2)
    frames.append(cat_freq)

    # Skill level frequency
    lvl_freq = skills_clean["skill_level"].value_counts().reset_index()
    lvl_freq.columns = ["value", "count"]
    lvl_freq["summary_type"] = "skill_level_frequency"
    lvl_freq["pct"] = (lvl_freq["count"] / len(skills_clean) * 100).round(2)
    frames.append(lvl_freq)

    summary = pd.concat(frames, ignore_index=True)[
        ["summary_type", "value", "count", "pct"]
    ]
    return summary


# ---------------------------------------------------------------------------
# D. Country Trends Clean
# ---------------------------------------------------------------------------

def clean_country_trends(country_ai_trends: pd.DataFrame) -> pd.DataFrame:
    """
    Return a clean copy of country_ai_trends with a period_type label.

    Parameters
    ----------
    country_ai_trends : raw country_ai_trends DataFrame

    Returns
    -------
    pd.DataFrame — 42 rows
    """
    df = country_ai_trends.copy()
    df["period_type"] = np.where(df["year"] <= 2024, "Historical", "Projected")
    return df


# ---------------------------------------------------------------------------
# E. Save processed datasets
# ---------------------------------------------------------------------------

def save_processed(jobs_clean: pd.DataFrame,
                   jobs_country_enriched: pd.DataFrame,
                   skills_clean: pd.DataFrame,
                   skill_summary: pd.DataFrame,
                   country_trends_clean: pd.DataFrame,
                   verbose: bool = True) -> None:
    """Write all processed datasets to data/processed/."""
    _ensure_dirs()
    files = {
        "jobs_clean.csv":              jobs_clean,
        "jobs_country_enriched.csv":   jobs_country_enriched,
        "skills_clean.csv":            skills_clean,
        "skill_summary.csv":           skill_summary,
        "country_trends_clean.csv":    country_trends_clean,
    }
    for fname, df in files.items():
        path = PROCESSED_DIR / fname
        df.to_csv(path, index=False)
        if verbose:
            print(f"  Saved {fname:<35} {df.shape[0]:>7,} rows x {df.shape[1]} cols  ->  {path.name}")


# ---------------------------------------------------------------------------
# F. Save export datasets (Power BI / dashboard-ready)
# ---------------------------------------------------------------------------

def save_exports(jobs_country_enriched: pd.DataFrame,
                 skills_clean: pd.DataFrame,
                 country_trends_clean: pd.DataFrame,
                 verbose: bool = True) -> None:
    """
    Write dashboard-ready export files to data/exports/.

    powerbi_jobs.csv            — full enriched job dataset
    powerbi_skills.csv          — skill-level dataset (independent)
    powerbi_country_trends.csv  — country aggregate trends
    """
    _ensure_dirs()
    files = {
        "powerbi_jobs.csv":            jobs_country_enriched,
        "powerbi_skills.csv":          skills_clean,
        "powerbi_country_trends.csv":  country_trends_clean,
    }
    for fname, df in files.items():
        path = EXPORTS_DIR / fname
        df.to_csv(path, index=False)
        if verbose:
            print(f"  Saved {fname:<35} {df.shape[0]:>7,} rows x {df.shape[1]} cols  ->  {path.name}")


# ---------------------------------------------------------------------------
# G. Full pipeline convenience function
# ---------------------------------------------------------------------------

def run_full_pipeline(ai_jobs: pd.DataFrame,
                      skills_demand: pd.DataFrame,
                      country_ai_trends: pd.DataFrame,
                      job_title_mapping: pd.DataFrame,
                      verbose: bool = True) -> dict:
    """
    Run the complete preprocessing pipeline and save all outputs.

    Returns a dict of all processed DataFrames.
    """
    if verbose:
        print("=== AI MarketLens - Preprocessing Pipeline ===\n")
        print("Step 1/5  Cleaning jobs...")
    jobs_clean = clean_jobs(ai_jobs, job_title_mapping)

    if verbose:
        print("Step 2/5  Building country-enriched dataset...")
    jobs_country_enriched = build_country_enriched(jobs_clean, country_ai_trends)

    if verbose:
        print("Step 3/5  Processing skills (independent — no direct join)...")
    skills_clean = clean_skills(skills_demand)
    skill_summary = build_skill_summary(skills_clean)

    if verbose:
        print("Step 4/5  Cleaning country trends...")
    country_trends_clean = clean_country_trends(country_ai_trends)

    if verbose:
        print("Step 5/5  Saving outputs...\n")
        print("  [data/processed/]")
    save_processed(jobs_clean, jobs_country_enriched, skills_clean,
                   skill_summary, country_trends_clean, verbose=verbose)

    if verbose:
        print("\n  [data/exports/]")
    save_exports(jobs_country_enriched, skills_clean,
                 country_trends_clean, verbose=verbose)

    if verbose:
        print("\nPipeline complete.")

    return {
        "jobs_clean":             jobs_clean,
        "jobs_country_enriched":  jobs_country_enriched,
        "skills_clean":           skills_clean,
        "skill_summary":          skill_summary,
        "country_trends_clean":   country_trends_clean,
    }
