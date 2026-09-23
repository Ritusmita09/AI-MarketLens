import sys, json
from pathlib import Path

print("=== PHASE 3 VALIDATION ===\n")

def check_file(path_str):
    p = Path(path_str)
    exists = p.exists()
    size   = f"{p.stat().st_size // 1024} KB" if exists else "MISSING"
    print(f"  {p.name:<36} exists={exists}  {size}")

print("--- Power BI docs ---")
for f in ["powerbi/POWERBI_SETUP.md","powerbi/POWERBI_DATA_MODEL.md",
          "powerbi/POWERBI_DAX_MEASURES.md","powerbi/powerbi_theme.json"]:
    check_file(f)

print("\n--- Streamlit app ---")
for f in [
    "dashboard/app.py",
    "dashboard/.streamlit/config.toml",
    "dashboard/utils/data.py",
    "dashboard/utils/charts.py",
    "dashboard/app_pages/overview.py",
    "dashboard/app_pages/salary.py",
    "dashboard/app_pages/job_market.py",
    "dashboard/app_pages/skills.py",
    "dashboard/app_pages/remote_work.py",
    "dashboard/app_pages/ml_insights.py",
    "dashboard/app_pages/data_explorer.py",
    "dashboard/app_pages/methodology.py",
    "dashboard/README.md",
]:
    check_file(f)

print("\n--- Web dashboard ---")
for f in ["web_dashboard/index.html","web_dashboard/css/style.css",
          "web_dashboard/js/charts.js","web_dashboard/js/app.js",
          "web_dashboard/README.md"]:
    check_file(f)

print("\n--- JSON data files ---")
all_ok = True
for name in ["kpis","salary","countries","skills","roles","remote","trends"]:
    p = Path(f"web_dashboard/data/{name}.json")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        keys = list(data.keys()) if isinstance(data, dict) else "(list)"
        print(f"  {name+'.json':<20} size={p.stat().st_size//1024} KB  keys={keys}")
    except Exception as e:
        print(f"  {name}.json  ERROR: {e}")
        all_ok = False

print("\n--- KPI values ---")
kpis = json.loads(Path("web_dashboard/data/kpis.json").read_text(encoding="utf-8"))
for k, v in kpis.items():
    print(f"  {k:<35} = {v}")

print(f"\nAll JSON valid: {all_ok}")
print("=== VALIDATION COMPLETE ===")
