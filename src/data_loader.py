"""
data_loader.py
--------------
Loads and validates the raw AI MarketLens dataset files.

All paths are resolved relative to the project root so the module
works regardless of the operating-system user or machine.

Raw files must NEVER be modified by this module.
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

# Resolve the project root as the parent of the src/ directory
_SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SRC_DIR.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "archive (1)"


def _raw(filename: str) -> Path:
    """Return the absolute path to a raw data file."""
    return RAW_DIR / filename


# ---------------------------------------------------------------------------
# Individual file loaders
# ---------------------------------------------------------------------------

def load_ai_jobs() -> pd.DataFrame:
    """Load ai_jobs.csv (50,000 rows × 14 columns)."""
    df = pd.read_csv(_raw("ai_jobs.csv"))
    return df


def load_skills_demand() -> pd.DataFrame:
    """Load skills_demand.csv (224,605 rows × 4 columns)."""
    df = pd.read_csv(_raw("skills_demand.csv"))
    return df


def load_country_ai_trends() -> pd.DataFrame:
    """Load country_ai_trends.csv (42 rows × 6 columns)."""
    df = pd.read_csv(_raw("country_ai_trends.csv"))
    return df


def load_job_title_mapping() -> pd.DataFrame:
    """Load job_title_mapping.csv (6 rows × 3 columns)."""
    df = pd.read_csv(_raw("job_title_mapping.csv"))
    return df


def load_data_dictionary() -> pd.DataFrame:
    """Load data_dictionary.csv (13 rows × 3 columns)."""
    df = pd.read_csv(_raw("data_dictionary.csv"))
    return df


# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------

EXPECTED_SHAPES = {
    "ai_jobs":             (50_000, 14),
    "skills_demand":       (224_605, 4),
    "country_ai_trends":   (42,     6),
    "job_title_mapping":   (6,      3),
    "data_dictionary":     (13,     3),
}

EXPECTED_COLUMNS = {
    "ai_jobs": [
        "job_id", "job_title", "company_type", "industry", "country", "city",
        "remote_type", "experience_level", "min_experience_years",
        "salary_min_usd", "salary_max_usd", "employment_type",
        "posted_year", "company_size",
    ],
    "skills_demand": ["job_id", "skill", "skill_category", "skill_level"],
    "country_ai_trends": [
        "country", "year", "total_ai_jobs", "avg_salary_usd",
        "remote_percentage", "top_skill",
    ],
    "job_title_mapping": ["job_title", "standardized_title", "role_category"],
    "data_dictionary": ["file", "column", "description"],
}


def validate_raw_files(verbose: bool = True) -> dict:
    """
    Load every raw file, check shape and columns, report missing values
    and duplicates.  Returns a dict keyed by table name with validation
    results.  Does NOT modify source files.
    """
    loaders = {
        "ai_jobs":           load_ai_jobs,
        "skills_demand":     load_skills_demand,
        "country_ai_trends": load_country_ai_trends,
        "job_title_mapping": load_job_title_mapping,
        "data_dictionary":   load_data_dictionary,
    }
    results = {}
    for name, loader in loaders.items():
        df = loader()
        expected_shape = EXPECTED_SHAPES[name]
        expected_cols  = EXPECTED_COLUMNS[name]
        results[name] = {
            "shape":          df.shape,
            "shape_ok":       df.shape == expected_shape,
            "cols_ok":        list(df.columns) == expected_cols,
            "missing_total":  int(df.isnull().sum().sum()),
            "duplicates":     int(df.duplicated().sum()),
        }
        if verbose:
            ok = "OK" if results[name]["shape_ok"] else "!!"
            print(
                f"  {ok} {name:<22} "
                f"shape={df.shape}  "
                f"missing={results[name]['missing_total']}  "
                f"dupes={results[name]['duplicates']}"
            )
    return results


# ---------------------------------------------------------------------------
# Convenience: load all at once
# ---------------------------------------------------------------------------

def load_all() -> dict:
    """Return a dict of all raw DataFrames keyed by short table name."""
    return {
        "ai_jobs":           load_ai_jobs(),
        "skills_demand":     load_skills_demand(),
        "country_ai_trends": load_country_ai_trends(),
        "job_title_mapping": load_job_title_mapping(),
        "data_dictionary":   load_data_dictionary(),
    }
