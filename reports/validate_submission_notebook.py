"""
reports/validate_submission_notebook.py
----------------------------------------
Executes the submission notebook from a clean kernel and reports results.

Usage (from project root):
    python reports/validate_submission_notebook.py

Outputs:
    reports/notebook_execution_report.json  — machine-readable results
    submission/Ritusmita_AI_MarketLens_validated.ipynb  — executed copy
"""

import json
import sys
import time
import pathlib
import subprocess
from datetime import datetime

NOTEBOOK_PATH   = pathlib.Path("submission/Ritusmita_AI_MarketLens.ipynb")
EXECUTED_PATH   = pathlib.Path("submission/Ritusmita_AI_MarketLens_validated.ipynb")
REPORT_JSON     = pathlib.Path("reports/notebook_execution_report.json")

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Business Problem",
    "Objectives",
    "Dataset Overview",
    "Data Dictionary",
    "Setup",
    "Data Loading",
    "Data Quality",
    "Cleaning",
    "Feature Engineering",
    "Exploratory Data Analysis",
    "Job Market",
    "Salary Analysis",
    "Country Analysis",
    "Remote Work",
    "Skills",
    "Historical vs Projected",
    "Statistical Analysis",
    "Machine Learning",
    "Model Evaluation",
    "Feature Importance",
    "Clustering",
    "Key Insights",
    "Business Recommendations",
    "Limitations",
    "Conclusion",
]

def main():
    print("=" * 65)
    print("AI MarketLens — Submission Notebook Validation")
    print(f"Notebook : {NOTEBOOK_PATH}")
    print(f"Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    # ── Step 1: Verify notebook file exists ──────────────────────────
    if not NOTEBOOK_PATH.exists():
        print(f"ERROR: Notebook not found at {NOTEBOOK_PATH}")
        sys.exit(1)

    nb_bytes = NOTEBOOK_PATH.stat().st_size
    print(f"\n[1] Notebook file found ({nb_bytes:,} bytes)")

    # ── Step 2: Quick structure check ────────────────────────────────
    nb = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    all_cells  = nb["cells"]
    code_cells = [c for c in all_cells if c["cell_type"] == "code"]
    md_cells   = [c for c in all_cells if c["cell_type"] == "markdown"]

    print(f"[2] Structure: {len(all_cells)} cells total "
          f"({len(code_cells)} code, {len(md_cells)} markdown)")

    # Check sections
    sections_found = []
    for c in md_cells:
        src = "".join(c["source"])
        for s in REQUIRED_SECTIONS:
            if s in src and s not in sections_found:
                sections_found.append(s)
    missing_sections = [s for s in REQUIRED_SECTIONS if s not in sections_found]
    print(f"[3] Sections: {len(sections_found)}/{len(REQUIRED_SECTIONS)} found", end="")
    if missing_sections:
        print(f"  MISSING: {missing_sections}")
    else:
        print(" OK")

    # ── Step 3: Execute with nbconvert ───────────────────────────────
    print(f"\n[4] Executing notebook from clean kernel ...")
    print("    (this may take 2-5 minutes)\n")
    t0 = time.time()

    cmd = [
        sys.executable, "-m", "nbconvert",
        "--to", "notebook",
        "--execute",
        f"--ExecutePreprocessor.timeout=360",
        "--ExecutePreprocessor.kernel_name=python3",
        "--output", str(EXECUTED_PATH.resolve()),
        str(NOTEBOOK_PATH.resolve()),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0

    # nbconvert prints progress to stderr even on success
    # Check for the "Writing N bytes" success line
    execution_ok = EXECUTED_PATH.exists() and "Writing" in result.stderr

    print(f"    Elapsed  : {elapsed:.1f}s")
    print(f"    Exit code: {result.returncode}")
    if execution_ok:
        print(f"    Output   : {EXECUTED_PATH} ({EXECUTED_PATH.stat().st_size:,} bytes)")
    else:
        print("    ERROR: executed notebook not created")
        if result.stderr:
            print("    stderr:", result.stderr[-500:])
        if result.stdout:
            print("    stdout:", result.stdout[-500:])

    # ── Step 4: Inspect execution results ────────────────────────────
    runtime_errors = []
    cells_executed = 0
    cells_with_output = 0
    cells_with_display = 0

    if execution_ok:
        nb_exec = json.loads(EXECUTED_PATH.read_text(encoding="utf-8"))
        for cell in nb_exec["cells"]:
            if cell["cell_type"] != "code":
                continue
            if cell.get("execution_count") is not None:
                cells_executed += 1
            outputs = cell.get("outputs", [])
            if outputs:
                cells_with_output += 1
            for out in outputs:
                if out.get("output_type") == "error":
                    runtime_errors.append({
                        "ename": out.get("ename", ""),
                        "evalue": out.get("evalue", ""),
                    })
                if out.get("output_type") == "display_data":
                    cells_with_display += 1

    print(f"\n[5] Execution results:")
    print(f"    Code cells total    : {len(code_cells)}")
    print(f"    Code cells executed : {cells_executed}")
    print(f"    Cells with output   : {cells_with_output}")
    print(f"    Cells with display  : {cells_with_display}")
    print(f"    Runtime errors      : {len(runtime_errors)}")

    if runtime_errors:
        print("    ERRORS:")
        for err in runtime_errors:
            print(f"      {err['ename']}: {err['evalue']}")

    # ── Step 5: Summary ──────────────────────────────────────────────
    passed = (
        execution_ok
        and cells_executed == len(code_cells)
        and len(runtime_errors) == 0
        and len(missing_sections) == 0
    )

    print("\n" + "=" * 65)
    status = "PASS" if passed else "FAIL"
    print(f"VALIDATION RESULT: {status}")
    print("=" * 65)

    # ── Step 6: Write JSON report ─────────────────────────────────────
    report = {
        "timestamp": datetime.now().isoformat(),
        "notebook": str(NOTEBOOK_PATH),
        "executed_notebook": str(EXECUTED_PATH),
        "passed": passed,
        "total_cells": len(all_cells),
        "code_cells": len(code_cells),
        "md_cells": len(md_cells),
        "cells_executed": cells_executed,
        "cells_with_output": cells_with_output,
        "cells_with_display": cells_with_display,
        "runtime_errors": runtime_errors,
        "sections_found": len(sections_found),
        "sections_required": len(REQUIRED_SECTIONS),
        "missing_sections": missing_sections,
        "execution_time_seconds": round(elapsed, 1),
    }
    REPORT_JSON.parent.mkdir(exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport saved: {REPORT_JSON}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
