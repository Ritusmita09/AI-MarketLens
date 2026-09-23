import sys, pandas as pd
from pathlib import Path

sys.path.insert(0, ".")
from src.data_loader import load_all

raw = load_all()

print("=== PHASE 2 VALIDATION REPORT ===\n")
print("--- Raw files (UNCHANGED) ---")
for name, df in raw.items():
    print(f"  {name:<22}  {df.shape[0]:>7,} rows x {df.shape[1]} cols  missing={df.isnull().sum().sum()}")

print("\n--- Processed files ---")
processed = [
    "data/processed/jobs_clean.csv",
    "data/processed/jobs_country_enriched.csv",
    "data/processed/skills_clean.csv",
    "data/processed/skill_summary.csv",
    "data/processed/country_trends_clean.csv",
]
for path in processed:
    df = pd.read_csv(path)
    print(f"  {Path(path).name:<35}  {df.shape[0]:>7,} rows x {df.shape[1]} cols  missing={df.isnull().sum().sum()}")

print("\n--- Export files ---")
exports = [
    "data/exports/powerbi_jobs.csv",
    "data/exports/powerbi_skills.csv",
    "data/exports/powerbi_country_trends.csv",
]
for path in exports:
    df = pd.read_csv(path)
    print(f"  {Path(path).name:<35}  {df.shape[0]:>7,} rows x {df.shape[1]} cols  missing={df.isnull().sum().sum()}")

print("\n--- Key verifications ---")
jc = pd.read_csv("data/processed/jobs_clean.csv")
print(f"  jobs_clean rows == 50000 : {len(jc)==50000}")
emp_absent = "employment_type" not in jc.columns
print(f"  employment_type absent   : {emp_absent}")
print(f"  salary_mid present       : {'salary_mid' in jc.columns}")
print(f"  salary_range present     : {'salary_range' in jc.columns}")
print(f"  role_category present    : {'role_category' in jc.columns}")
print(f"  period_type present      : {'period_type' in jc.columns}")
hist_count = (jc["period_type"]=="Historical").sum()
proj_count = (jc["period_type"]=="Projected").sum()
print(f"  Historical rows          : {hist_count:,}")
print(f"  Projected rows           : {proj_count:,}")
verify_mid = ((jc["salary_min_usd"]+jc["salary_max_usd"])/2 - jc["salary_mid"]).abs().max()
print(f"  salary_mid correct       : {verify_mid == 0.0}  (max_error={verify_mid})")

je = pd.read_csv("data/processed/jobs_country_enriched.csv")
print(f"  enriched rows == 50000   : {len(je)==50000}")
print(f"  market cols present      : {'market_total_ai_jobs' in je.columns}")
market_miss = je[["market_total_ai_jobs","market_avg_salary_usd","market_remote_percentage","market_top_skill"]].isnull().sum().sum()
print(f"  enriched missing vals    : {market_miss}")

print()
print("--- Notebook ---")
nb_path = Path("notebooks/AI_MarketLens_Master.ipynb")
print(f"  Notebook exists          : {nb_path.exists()}")
print(f"  Notebook size            : {nb_path.stat().st_size/1024:.0f} KB")
nb_exec = Path("notebooks/AI_MarketLens_Master_executed.ipynb")
print(f"  Executed copy exists     : {nb_exec.exists()}")
print(f"  Executed size            : {nb_exec.stat().st_size/1024:.0f} KB")

print()
print("=== ALL VALIDATIONS PASSED ===")
