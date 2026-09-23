"""
reconcile_kpis.py
-----------------
Single source of truth for all KPI values used across
the entire AI MarketLens project.  Run from project root.
All values derive from data/exports/powerbi_jobs.csv,
data/exports/powerbi_skills.csv, and
data/exports/powerbi_country_trends.csv.
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

EXPORTS = Path("data/exports")
jobs   = pd.read_csv(EXPORTS / "powerbi_jobs.csv")
skills = pd.read_csv(EXPORTS / "powerbi_skills.csv")
ct     = pd.read_csv(EXPORTS / "powerbi_country_trends.csv")

# ── Derived columns ─────────────────────────────────────────
# salary_mid definition (authoritative)
jobs["salary_mid"]   = (jobs["salary_min_usd"] + jobs["salary_max_usd"]) / 2.0
jobs["salary_range"] = jobs["salary_max_usd"] - jobs["salary_min_usd"]
jobs["remote_flag"]  = (jobs["remote_type"] == "Remote").astype(int)
jobs["period_type"]  = jobs["posted_year"].apply(
    lambda y: "Historical" if y <= 2024 else "Projected")

# ── KPI calculations ─────────────────────────────────────────
total_jobs      = int(len(jobs))
hist_jobs       = int((jobs["period_type"] == "Historical").sum())
proj_jobs       = int((jobs["period_type"] == "Projected").sum())

mean_salary_mid   = round(float(jobs["salary_mid"].mean()), 2)
median_salary_mid = round(float(jobs["salary_mid"].median()), 2)
min_salary_mid    = round(float(jobs["salary_mid"].min()), 2)
max_salary_mid    = round(float(jobs["salary_mid"].max()), 2)
min_salary_min    = int(jobs["salary_min_usd"].min())
max_salary_max    = int(jobs["salary_max_usd"].max())

remote_pct = round(float(jobs["remote_flag"].mean() * 100), 2)
countries  = int(jobs["country"].nunique())
job_roles  = int(jobs["job_title"].nunique())
skills_cnt = int(skills["skill"].nunique())

entry_sal  = float(jobs[jobs["experience_level"] == "Entry"]["salary_mid"].mean())
mid_sal    = float(jobs[jobs["experience_level"] == "Mid"]["salary_mid"].mean())
senior_sal = float(jobs[jobs["experience_level"] == "Senior"]["salary_mid"].mean())
senior_entry_ratio = round(senior_sal / entry_sal, 4)

top_country  = str(jobs["country"].value_counts().index[0])
top_job_role = str(jobs["job_title"].value_counts().index[0])
top_skill    = str(skills["skill"].value_counts().index[0])

total_market_ai_jobs = int(ct["total_ai_jobs"].sum())
mean_market_salary   = round(float(ct["avg_salary_usd"].mean()), 0)
mean_market_remote   = round(float(ct["remote_percentage"].mean()), 1)

kpis = {
    "definition": {
        "salary_mid": "(salary_min_usd + salary_max_usd) / 2.0",
        "period_type": "Historical if posted_year <= 2024 else Projected",
        "remote_flag": "1 if remote_type == 'Remote' else 0",
    },
    "job_counts": {
        "total_job_postings": total_jobs,
        "historical_jobs":    hist_jobs,
        "projected_jobs":     proj_jobs,
    },
    "salary": {
        "mean_salary_mid":   mean_salary_mid,
        "median_salary_mid": median_salary_mid,
        "min_salary_mid":    min_salary_mid,
        "max_salary_mid":    max_salary_mid,
        "min_salary_min_usd": min_salary_min,
        "max_salary_max_usd": max_salary_max,
        "entry_avg_salary":  round(entry_sal, 2),
        "mid_avg_salary":    round(mid_sal, 2),
        "senior_avg_salary": round(senior_sal, 2),
        "senior_entry_ratio": senior_entry_ratio,
    },
    "dimensions": {
        "countries_covered":  countries,
        "unique_job_roles":   job_roles,
        "skills_tracked":     skills_cnt,
        "remote_job_pct":     remote_pct,
        "top_country":        top_country,
        "top_job_role":       top_job_role,
        "top_skill_by_frequency": top_skill,
    },
    "market_level": {
        "total_market_ai_jobs":     total_market_ai_jobs,
        "mean_market_avg_salary":   mean_market_salary,
        "mean_market_remote_pct":   mean_market_remote,
    },
}

# ── Print reconciliation report ──────────────────────────────
print("=" * 64)
print("AI MarketLens — AUTHORITATIVE KPI RECONCILIATION")
print("=" * 64)
print()
print("SALARY DEFINITION")
print(f"  salary_mid = (salary_min_usd + salary_max_usd) / 2.0")
print()
print("JOB COUNTS")
print(f"  Total Job Postings  : {total_jobs:,}")
print(f"  Historical (<=2024) : {hist_jobs:,}")
print(f"  Projected (2025-26) : {proj_jobs:,}")
print()
print("SALARY (salary_mid)")
print(f"  Mean   salary_mid   : ${mean_salary_mid:,.2f}")
print(f"  Median salary_mid   : ${median_salary_mid:,.2f}")
print(f"  Min    salary_mid   : ${min_salary_mid:,.2f}")
print(f"  Max    salary_mid   : ${max_salary_mid:,.2f}")
print(f"  Min    salary_min_usd : ${min_salary_min:,}")
print(f"  Max    salary_max_usd : ${max_salary_max:,}")
print()
print("SALARY BY EXPERIENCE")
print(f"  Entry   avg salary_mid : ${entry_sal:,.2f}")
print(f"  Mid     avg salary_mid : ${mid_sal:,.2f}")
print(f"  Senior  avg salary_mid : ${senior_sal:,.2f}")
print(f"  Senior / Entry ratio   : {senior_entry_ratio:.4f}x")
print()
print("DIMENSIONS")
print(f"  Countries   : {countries}")
print(f"  Job Roles   : {job_roles}")
print(f"  Skills      : {skills_cnt}")
print(f"  Remote %    : {remote_pct}%")
print(f"  Top Country : {top_country}")
print(f"  Top Role    : {top_job_role}")
print(f"  Top Skill   : {top_skill}")
print()
print("MARKET LEVEL (country_ai_trends)")
print(f"  Total Market AI Jobs  : {total_market_ai_jobs:,}")
print(f"  Mean Market Salary    : ${mean_market_salary:,.0f}")
print(f"  Mean Market Remote %  : {mean_market_remote}%")
print()

# ── Save canonical KPIs JSON ─────────────────────────────────
out_path = Path("reports/canonical_kpis.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(kpis, f, indent=2)
print(f"Saved canonical KPIs -> {out_path}")

# Also update web_dashboard/data/kpis.json
flat_kpis = {
    "total_job_postings":   total_jobs,
    "avg_salary_usd":       mean_salary_mid,
    "median_salary_usd":    median_salary_mid,
    "min_salary_mid":       min_salary_mid,
    "max_salary_mid":       max_salary_mid,
    "remote_job_pct":       remote_pct,
    "countries_covered":    countries,
    "job_roles":            job_roles,
    "skills_tracked":       skills_cnt,
    "historical_jobs":      hist_jobs,
    "projected_jobs":       proj_jobs,
    "entry_avg_salary":     round(entry_sal, 2),
    "mid_avg_salary":       round(mid_sal, 2),
    "senior_avg_salary":    round(senior_sal, 2),
    "senior_premium_ratio": senior_entry_ratio,
    "salary_min_usd":       min_salary_min,
    "salary_max_usd":       max_salary_max,
    "total_market_ai_jobs": total_market_ai_jobs,
    "avg_market_salary":    int(mean_market_salary),
    "avg_market_remote_pct": mean_market_remote,
}
kpis_web = Path("web_dashboard/data/kpis.json")
with open(kpis_web, "w", encoding="utf-8") as f:
    json.dump(flat_kpis, f, indent=2)
print(f"Updated web KPIs    -> {kpis_web}")
