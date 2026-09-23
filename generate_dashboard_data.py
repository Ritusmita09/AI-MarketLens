"""
generate_dashboard_data.py
--------------------------
Generates aggregated JSON files for the HTML/JS web dashboard.
All values are derived from the Phase 2 processed exports.
Run from project root: python generate_dashboard_data.py
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
EXPORTS_DIR  = Path("data/exports")
WEB_DATA_DIR = Path("web_dashboard/data")
WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load exports
# ---------------------------------------------------------------------------
jobs   = pd.read_csv(EXPORTS_DIR / "powerbi_jobs.csv")
skills = pd.read_csv(EXPORTS_DIR / "powerbi_skills.csv")
ct     = pd.read_csv(EXPORTS_DIR / "powerbi_country_trends.csv")

# Ensure derived columns are present
if "remote_flag" not in jobs.columns:
    jobs["remote_flag"] = (jobs["remote_type"] == "Remote").astype(int)
if "salary_mid" not in jobs.columns:
    jobs["salary_mid"] = (jobs["salary_min_usd"] + jobs["salary_max_usd"]) / 2
if "period_type" not in jobs.columns:
    jobs["period_type"] = jobs["posted_year"].apply(
        lambda y: "Historical" if y <= 2024 else "Projected")

print(f"Loaded  jobs={jobs.shape}  skills={skills.shape}  country_trends={ct.shape}")


def save_json(data, filename):
    path = WEB_DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  Saved {filename:<35} {path.stat().st_size // 1024} KB")


def salary_by(col):
    """Aggregate salary_mid statistics grouped by col."""
    return (
        jobs.groupby(col)["salary_mid"]
        .agg(avg="mean", median="median", min_val="min", max_val="max")
        .round(0)
        .reset_index()
        .rename(columns={"min_val": "min", "max_val": "max"})
        .to_dict(orient="records")
    )


def yoy_growth(df):
    """Compute year-over-year growth % for total_ai_jobs per country."""
    result = []
    for country_name in df["country"].unique():
        sub = df[df["country"] == country_name].sort_values("year")
        for i in range(1, len(sub)):
            prev = sub.iloc[i - 1]
            curr = sub.iloc[i]
            growth = None
            if prev["total_ai_jobs"] > 0:
                growth = round(
                    (curr["total_ai_jobs"] - prev["total_ai_jobs"])
                    / prev["total_ai_jobs"] * 100, 1
                )
            result.append({
                "country":      country_name,
                "year":         int(curr["year"]),
                "period_type":  curr["period_type"],
                "yoy_growth_pct": growth,
            })
    return result


# ---------------------------------------------------------------------------
# 1. kpis.json
# ---------------------------------------------------------------------------
entry_sal  = float(jobs[jobs["experience_level"] == "Entry"]["salary_mid"].mean())
senior_sal = float(jobs[jobs["experience_level"] == "Senior"]["salary_mid"].mean())

kpis = {
    "total_job_postings":   int(len(jobs)),
    "avg_salary_usd":       round(float(jobs["salary_mid"].mean()), 0),
    "median_salary_usd":    round(float(jobs["salary_mid"].median()), 0),
    "remote_job_pct":       round(float((jobs["remote_type"] == "Remote").mean() * 100), 1),
    "countries_covered":    int(jobs["country"].nunique()),
    "job_roles":            int(jobs["job_title"].nunique()),
    "skills_tracked":       int(skills["skill"].nunique()),
    "historical_jobs":      int((jobs["period_type"] == "Historical").sum()),
    "projected_jobs":       int((jobs["period_type"] == "Projected").sum()),
    "entry_avg_salary":     round(entry_sal, 0),
    "senior_avg_salary":    round(senior_sal, 0),
    "senior_premium_ratio": round(senior_sal / entry_sal, 2),
    "salary_min_usd":       int(jobs["salary_min_usd"].min()),
    "salary_max_usd":       int(jobs["salary_max_usd"].max()),
    "total_market_ai_jobs": int(ct["total_ai_jobs"].sum()),
    "avg_market_salary":    int(ct["avg_salary_usd"].mean()),
    "avg_market_remote_pct": round(float(ct["remote_percentage"].mean()), 1),
}
save_json(kpis, "kpis.json")

# ---------------------------------------------------------------------------
# 2. salary.json
# ---------------------------------------------------------------------------
salary_data = {
    "by_experience":   salary_by("experience_level"),
    "by_country":      salary_by("country"),
    "by_job_title":    salary_by("job_title"),
    "by_industry":     salary_by("industry"),
    "by_remote_type":  salary_by("remote_type"),
    "by_company_type": salary_by("company_type"),
    "by_company_size": salary_by("company_size"),
    "by_year": (
        jobs.groupby(["posted_year", "period_type"])["salary_mid"]
        .agg(avg="mean", median="median").round(0).reset_index()
        .to_dict(orient="records")
    ),
}
save_json(salary_data, "salary.json")

# ---------------------------------------------------------------------------
# 3. countries.json
# ---------------------------------------------------------------------------
country_sample = (
    jobs.groupby("country")
    .agg(
        job_count=("job_id", "count"),
        avg_salary=("salary_mid", "mean"),
    )
    .round(0).reset_index()
    .to_dict(orient="records")
)
# Add remote_pct separately to avoid lambda in agg
remote_by_country = (
    jobs.groupby("country")["remote_flag"]
    .mean().mul(100).round(1).reset_index(name="remote_pct")
)
country_sample_df = pd.DataFrame(country_sample).merge(remote_by_country, on="country")

countries_data = {
    "sample_jobs_by_country":  country_sample_df.to_dict(orient="records"),
    "market_trends":           ct.to_dict(orient="records"),
    "market_by_country_year":  ct[[
        "country", "year", "total_ai_jobs", "avg_salary_usd",
        "remote_percentage", "top_skill", "period_type"
    ]].to_dict(orient="records"),
}
save_json(countries_data, "countries.json")

# ---------------------------------------------------------------------------
# 4. skills.json
# ---------------------------------------------------------------------------
skill_freq        = skills["skill"].value_counts().reset_index()
skill_freq.columns = ["skill", "count"]
skill_freq["pct"] = (skill_freq["count"] / len(skills) * 100).round(2)

cat_freq           = skills["skill_category"].value_counts().reset_index()
cat_freq.columns   = ["category", "count"]

level_freq         = skills["skill_level"].value_counts().reset_index()
level_freq.columns = ["level", "count"]

skills_data = {
    "skill_frequency":           skill_freq.to_dict(orient="records"),
    "category_frequency":        cat_freq.to_dict(orient="records"),
    "level_frequency":           level_freq.to_dict(orient="records"),
    "top_skill_by_country_year": ct[["country", "year", "top_skill", "period_type"]].to_dict(orient="records"),
    "data_note": (
        "skills_demand.job_id does not reliably match ai_jobs.job_id (4.1% overlap). "
        "Skills are analyzed as an independent dataset."
    ),
}
save_json(skills_data, "skills.json")

# ---------------------------------------------------------------------------
# 5. roles.json
# ---------------------------------------------------------------------------
roles_data = {
    "job_title_counts": (
        jobs["job_title"].value_counts().reset_index()
        .rename(columns={"job_title": "role"}).to_dict(orient="records")
    ),
    "role_category_counts": (
        jobs["role_category"].value_counts().reset_index()
        .rename(columns={"role_category": "category"}).to_dict(orient="records")
    ),
    "by_year": (
        jobs.groupby(["posted_year", "job_title", "period_type"])
        .size().reset_index(name="count").to_dict(orient="records")
    ),
    "salary_by_role":   salary_by("job_title"),
    "industry_counts": (
        jobs["industry"].value_counts().reset_index()
        .rename(columns={"industry": "industry"}).to_dict(orient="records")
    ),
    "company_type_counts": (
        jobs["company_type"].value_counts().reset_index().to_dict(orient="records")
    ),
    "company_size_counts": (
        jobs["company_size"].value_counts().reset_index().to_dict(orient="records")
    ),
    "top_cities": (
        jobs[jobs["city"] != "Remote"]["city"]
        .value_counts().head(15).reset_index()
        .rename(columns={"city": "city"}).to_dict(orient="records")
    ),
}
save_json(roles_data, "roles.json")

# ---------------------------------------------------------------------------
# 6. remote.json
# ---------------------------------------------------------------------------
remote_data = {
    "overall": (
        jobs["remote_type"].value_counts().reset_index().to_dict(orient="records")
    ),
    "by_year": (
        jobs.groupby(["posted_year", "period_type"])["remote_flag"]
        .mean().mul(100).round(1).reset_index(name="remote_pct")
        .to_dict(orient="records")
    ),
    "by_country": (
        jobs.groupby("country")["remote_type"]
        .value_counts(normalize=True).mul(100).round(1)
        .reset_index(name="pct").to_dict(orient="records")
    ),
    "by_experience": (
        jobs.groupby("experience_level")["remote_flag"]
        .mean().mul(100).round(1).reset_index(name="remote_pct")
        .to_dict(orient="records")
    ),
    "by_industry": (
        jobs.groupby("industry")["remote_flag"]
        .mean().mul(100).round(1).reset_index(name="remote_pct")
        .to_dict(orient="records")
    ),
    "market_remote_pct": ct[[
        "country", "year", "remote_percentage", "period_type"
    ]].to_dict(orient="records"),
}
save_json(remote_data, "remote.json")

# ---------------------------------------------------------------------------
# 7. trends.json
# ---------------------------------------------------------------------------
trends_data = {
    "jobs_by_year": (
        jobs.groupby(["posted_year", "period_type"]).size()
        .reset_index(name="count").to_dict(orient="records")
    ),
    "market_total_by_year": (
        ct.groupby(["year", "period_type"])["total_ai_jobs"]
        .sum().reset_index(name="total").to_dict(orient="records")
    ),
    "market_by_country_year": ct.to_dict(orient="records"),
    "yoy_market_growth": yoy_growth(ct),
}
save_json(trends_data, "trends.json")

print("\nAll 7 JSON data files generated.")
print(f"Output: {WEB_DATA_DIR.resolve()}")
