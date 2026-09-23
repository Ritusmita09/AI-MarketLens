"""
fix_notebook_static2.py
-----------------------
Second pass: fixes remaining 10 pyright issues after fix_notebook_static.py
Run from project root: python fix_notebook_static2.py
"""
import json
import pathlib

NB_PATH = pathlib.Path("submission/Ritusmita_AI_MarketLens.ipynb")
nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
cells = nb["cells"]

def get_src(cell):
    return "".join(cell["source"])

def set_src(cell, s):
    cell["source"] = s.splitlines(keepends=True)

fixes = 0

# ─────────────────────────────────────────────────────────────────────────
# FIX A: city_counts value_counts — use .loc to avoid ambiguous ndarray
#   was: pd.Series(jobs[jobs['city'] != 'Remote']['city'].value_counts())
#   fix: pd.Series(jobs.loc[jobs['city'] != 'Remote', 'city'].value_counts())
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "_city_vc: pd.Series = pd.Series(jobs[jobs['city'] != 'Remote']['city'].value_counts())" in src:
        new = src.replace(
            "_city_vc: pd.Series = pd.Series(jobs[jobs['city'] != 'Remote']['city'].value_counts())",
            "_city_vc: pd.Series = pd.Series(jobs.loc[jobs['city'] != 'Remote', 'city'].value_counts())"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX A [cell {i}]: city_counts use .loc")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX B: subset['job_title'].value_counts() in hist/proj loop — use .loc
#   was: subset['job_title'].value_counts()
#   fix: subset.loc[:, 'job_title'].value_counts()
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "_vc: pd.Series = pd.Series(subset['job_title'].value_counts())" in src:
        new = src.replace(
            "_vc: pd.Series = pd.Series(subset['job_title'].value_counts())",
            "_vc: pd.Series = pd.Series(subset.loc[:, 'job_title'].value_counts())"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX B [cell {i}]: subset value_counts use .loc[:, 'job_title']")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX C: map(dict) — use pd.Series(exp_map) instead of dict directly
#   was: jobs_hist_ml['experience_level'].map(exp_map).tolist()
#   fix: jobs_hist_ml['experience_level'].map(pd.Series(exp_map)).tolist()
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "np.array(jobs_hist_ml['experience_level'].map(exp_map).tolist()" in src:
        new = src.replace(
            "np.array(jobs_hist_ml['experience_level'].map(exp_map).tolist(), dtype=float)",
            "np.array(jobs_hist_ml['experience_level'].map(pd.Series(exp_map)).tolist(), dtype=float)"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX C [cell {i}]: map(dict) -> map(pd.Series(dict))")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX D: X_train.shape[0] — build_ml_feature_matrix return type is list to pyright
#   add explicit np.ndarray annotation at the assignment
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "strat_col: np.ndarray = jobs_hist_ml['experience_level'].to_numpy()" in src and \
       "X_train, X_test, y_train, y_test = train_test_split(" in src:
        new = src.replace(
            "X_train, X_test, y_train, y_test = train_test_split(\n    X_full, y, test_size=0.2, random_state=42, stratify=strat_col)",
            "X_train_raw, X_test_raw, y_train, y_test = train_test_split(\n    X_full, y, test_size=0.2, random_state=42, stratify=strat_col)\n"
            "X_train: np.ndarray = np.asarray(X_train_raw)\n"
            "X_test:  np.ndarray = np.asarray(X_test_raw)"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX D [cell {i}]: X_train/X_test explicit np.ndarray annotation")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX E: grp["salary_mid"].mean() — pyright sees grp as DataFrame|Series
#   Replace float(grp[...].mean()) with explicit numpy scalar
#   was: _mean_v = float(grp["salary_mid"].mean())
#        _med_v  = float(grp["salary_mid"].median())
#   fix: use np.float64 which pyright accepts from ndarray mean/median
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if '_mean_v = float(grp["salary_mid"].mean())' in src:
        new = src.replace(
            '_mean_v = float(grp["salary_mid"].mean())\n'
            '    _med_v  = float(grp["salary_mid"].median())',
            '_sal_arr = jobs.loc[jobs["experience_level"]==exp, "salary_mid"].to_numpy(dtype=float)\n'
            '    _mean_v: float = float(_sal_arr.mean())\n'
            '    _med_v:  float = float(_sal_arr.mean())'
        )
        # Oops — mean twice. Use correct:
        new = src.replace(
            '_mean_v = float(grp["salary_mid"].mean())\n'
            '    _med_v  = float(grp["salary_mid"].median())',
            '_sal_arr = jobs.loc[jobs["experience_level"]==exp, "salary_mid"].to_numpy(dtype=float)\n'
            '    _mean_v: float = float(_sal_arr.mean())\n'
            '    _med_v:  float = float(float(np.median(_sal_arr)))'
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX E [cell {i}]: grp salary mean/median via .loc + to_numpy()")
        break

print(f"\nTotal fixes applied: {fixes}")
NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Saved {NB_PATH} ({NB_PATH.stat().st_size // 1024} KB)")
