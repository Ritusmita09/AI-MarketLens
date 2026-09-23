"""
data.py — Cached data loading for the AI MarketLens Streamlit app.
All data is loaded from data/exports/ (Phase 2 outputs).
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Ensure project root is on path
_DASHBOARD_DIR = Path(__file__).resolve().parent.parent
_PROJECT_ROOT  = _DASHBOARD_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

EXPORTS_DIR = _PROJECT_ROOT / "data" / "exports"


import streamlit as st


@st.cache_data(ttl=3600)
def load_jobs() -> pd.DataFrame:
    """Load the country-enriched jobs dataset (50,000 rows)."""
    df = pd.read_csv(EXPORTS_DIR / "powerbi_jobs.csv")
    # Ensure derived columns
    if "remote_flag" not in df.columns:
        df["remote_flag"] = (df["remote_type"] == "Remote").astype(int)
    if "salary_mid" not in df.columns:
        df["salary_mid"] = (df["salary_min_usd"] + df["salary_max_usd"]) / 2
    if "period_type" not in df.columns:
        df["period_type"] = df["posted_year"].apply(
            lambda y: "Historical" if y <= 2024 else "Projected")
    return df


@st.cache_data(ttl=3600)
def load_skills() -> pd.DataFrame:
    """Load the skills dataset (224,605 rows — independent from jobs)."""
    return pd.read_csv(EXPORTS_DIR / "powerbi_skills.csv")


@st.cache_data(ttl=3600)
def load_country_trends() -> pd.DataFrame:
    """Load the country AI trends dataset (42 rows)."""
    df = pd.read_csv(EXPORTS_DIR / "powerbi_country_trends.csv")
    if "period_type" not in df.columns:
        df["period_type"] = df["year"].apply(
            lambda y: "Historical" if y <= 2024 else "Projected")
    return df


@st.cache_data(ttl=3600)
def compute_kpis(jobs: pd.DataFrame, skills: pd.DataFrame,
                 country_trends: pd.DataFrame) -> dict:
    """Compute all top-level KPIs from the loaded data."""
    entry_sal  = jobs[jobs["experience_level"] == "Entry"]["salary_mid"].mean()
    senior_sal = jobs[jobs["experience_level"] == "Senior"]["salary_mid"].mean()
    return {
        "total_job_postings":   len(jobs),
        "avg_salary":           round(jobs["salary_mid"].mean(), 0),
        "median_salary":        round(jobs["salary_mid"].median(), 0),
        "min_salary":           int(jobs["salary_min_usd"].min()),
        "max_salary":           int(jobs["salary_max_usd"].max()),
        "remote_job_pct":       round((jobs["remote_type"] == "Remote").mean() * 100, 1),
        "countries_covered":    jobs["country"].nunique(),
        "job_roles":            jobs["job_title"].nunique(),
        "skills_tracked":       skills["skill"].nunique(),
        "historical_jobs":      int((jobs["period_type"] == "Historical").sum()),
        "projected_jobs":       int((jobs["period_type"] == "Projected").sum()),
        "entry_avg_salary":     round(entry_sal, 0),
        "senior_avg_salary":    round(senior_sal, 0),
        "senior_premium_ratio": round(senior_sal / entry_sal, 2),
        "total_market_ai_jobs": int(country_trends["total_ai_jobs"].sum()),
        "avg_market_salary":    int(country_trends["avg_salary_usd"].mean()),
    }
