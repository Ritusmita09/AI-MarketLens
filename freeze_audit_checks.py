"""freeze_audit_checks.py — runs all final freeze audit checks"""
import json, pathlib, os

# ── Canonical KPI verification ────────────────────────────────────────────
kpis = json.loads(pathlib.Path("reports/canonical_kpis.json").read_text(encoding="utf-8"))
S = kpis["salary"]; J = kpis["job_counts"]; D = kpis["dimensions"]; M = kpis["market_level"]

print("=== CANONICAL KPI VERIFICATION ===")
checks = [
    ("Total Job Postings",     J["total_job_postings"],             50000),
    ("Historical Jobs",        J["historical_jobs"],                35815),
    ("Projected Jobs",         J["projected_jobs"],                 14185),
    ("Mean Salary Midpoint",   round(S["mean_salary_mid"],2),       110864.89),
    ("Median Salary Midpoint", round(S["median_salary_mid"],2),     107565.25),
    ("Entry Avg Salary",       round(S["entry_avg_salary"],2),      67473.51),
    ("Mid Avg Salary",         round(S["mid_avg_salary"],2),        107507.12),
    ("Senior Avg Salary",      round(S["senior_avg_salary"],2),     157490.18),
    ("Senior/Entry Ratio",     round(S["senior_entry_ratio"],4),    2.3341),
    ("Remote Job %",           D["remote_job_pct"],                 32.96),
    ("Countries",              D["countries_covered"],              6),
    ("Job Roles",              D["unique_job_roles"],               6),
    ("Skills",                 D["skills_tracked"],                 11),
    ("Top Country",            D["top_country"],                    "UK"),
    ("Top Job Role",           D["top_job_role"],                   "MLOps Engineer"),
    ("Top Skill",              D["top_skill_by_frequency"],         "AWS"),
    ("Total Market AI Jobs",   M["total_market_ai_jobs"],           1734522),
]
kpi_ok = True
for name, actual, expected in checks:
    ok = (actual == expected)
    if not ok: kpi_ok = False
    print(f"  {'OK  ' if ok else 'FAIL'} {name}: {actual}  (expected {expected})")
print(f"KPI result: {'ALL PASS' if kpi_ok else 'FAILURES FOUND'}\n")

# ── Submission package verification ──────────────────────────────────────
print("=== SUBMISSION PACKAGE ===")
sub_dir = pathlib.Path("submission")
allowed = {
    "Ritusmita_AI_MarketLens.ipynb",
    "requirements.txt",
    "Ritusmita_AI_MarketLens_ProjectReport.docx",
    "README.md",
}
actual_files = {f.name for f in sub_dir.iterdir() if f.is_file()}
extra   = actual_files - allowed
missing = allowed - actual_files

for f in sorted(allowed):
    p = sub_dir / f
    exists = p.exists()
    size   = p.stat().st_size if exists else 0
    print(f"  {'OK  ' if exists else 'MISS'} {f}  ({size:,} bytes)")

if extra:
    print(f"  EXTRA FILES (must remove): {sorted(extra)}")
else:
    print("  No extra files in submission/")

print(f"Package result: {'PASS' if not missing and not extra else 'FAIL'}\n")

# ── Timestamp check ───────────────────────────────────────────────────────
main_nb   = sub_dir / "Ritusmita_AI_MarketLens.ipynb"
backup_nb = sub_dir / "Ritusmita_AI_MarketLens_before_error_fix.ipynb"
print("=== TIMESTAMP CHECK ===")
if main_nb.exists():
    print(f"  Main notebook  mtime: {os.path.getmtime(main_nb):.0f}  size: {main_nb.stat().st_size:,}")
if backup_nb.exists():
    print(f"  Backup notebook mtime: {os.path.getmtime(backup_nb):.0f}  size: {backup_nb.stat().st_size:,}")
    if main_nb.exists():
        newer = os.path.getmtime(main_nb) > os.path.getmtime(backup_nb)
        print(f"  Main is newer than backup: {newer}")
else:
    print("  Backup is NOT in submission/ (correct — backup is present but not in 4-file package)")
