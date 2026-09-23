"""
fix_notebook_static.py
-----------------------
Fixes all 90 pyright static-analysis issues in the submission notebook.
Run from project root: python fix_notebook_static.py
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
# FIX 1: plt.Rectangle → from matplotlib.patches import Rectangle
#   Cell with top_skill heatmap grid (nb index ~40)
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "plt.Rectangle((j, i)" in src:
        new = src.replace(
            "ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True,",
            "from matplotlib.patches import Rectangle as _Rect\n        ax.add_patch(_Rect((j, i), 1, 1, fill=True,"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 1 [cell {i}]: plt.Rectangle -> matplotlib.patches.Rectangle")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 2a: groupby().size().reset_index(name='count') for year_counts
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "year_counts = jobs.groupby(" in src and "period_type" in src and "reset_index(name=" in src:
        new = src.replace(
            "year_counts = jobs.groupby(['posted_year','period_type']).size().reset_index(name='count')",
            "_ys = jobs.groupby(['posted_year', 'period_type']).size().reset_index()\n"
            "year_counts: pd.DataFrame = pd.DataFrame(_ys).rename(columns={0: 'count'})"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 2a [cell {i}]: year_counts groupby.size().reset_index(name=)")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 2b: groupby().size().reset_index(name='count') for country_year
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "country_year = jobs.groupby(" in src and "reset_index(name=" in src:
        new = src.replace(
            "country_year = jobs.groupby(['country','posted_year']).size().reset_index(name='count')",
            "_cy = jobs.groupby(['country', 'posted_year']).size().reset_index()\n"
            "country_year: pd.DataFrame = pd.DataFrame(_cy).rename(columns={0: 'count'})"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 2b [cell {i}]: country_year groupby.size().reset_index(name=)")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 3: groupby mean().reindex(order) — salary by experience
#   salary_exp = jobs.groupby('experience_level')['salary_mid'].mean().reindex(order)
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "salary_exp = jobs.groupby('experience_level')['salary_mid'].mean().reindex(order)" in src:
        new = src.replace(
            "salary_exp = jobs.groupby('experience_level')['salary_mid'].mean().reindex(order)",
            "_sal_exp_raw = jobs.groupby('experience_level')['salary_mid'].mean()\n"
            "salary_exp: pd.Series = pd.Series(_sal_exp_raw).reindex(order)"
        )
        # Also fix the for loop that iterates salary_exp.items()
        # axes[1].bar iterates salary_exp.index / salary_exp.values  — fine after cast
        set_src(c, new)
        fixes += 1
        print(f"  FIX 3 [cell {i}]: salary_exp groupby mean().reindex()")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 4: groupby median().sort_values(ascending=False).index — order_c
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "order_c = jobs.groupby('country')['salary_mid'].median().sort_values(ascending=False).index.tolist()" in src:
        new = src.replace(
            "order_c = jobs.groupby('country')['salary_mid'].median().sort_values(ascending=False).index.tolist()",
            "_oc: pd.Series = pd.Series(jobs.groupby('country')['salary_mid'].median())\n"
            "order_c: list = _oc.sort_values(ascending=False).index.tolist()"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 4 [cell {i}]: order_c groupby median().sort_values()")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 5: .agg([...]).round(0).sort_values('mean', ascending=False)
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "sort_values('mean',ascending=False)" in src and "agg(['mean','median'])" in src:
        new = src.replace(
            "print(jobs.groupby('country')['salary_mid'].agg(['mean','median']).round(0).sort_values('mean',ascending=False))",
            "_sal_ctry: pd.DataFrame = pd.DataFrame(jobs.groupby('country')['salary_mid'].agg(['mean','median'])).round(0)\n"
            "print(_sal_ctry.sort_values('mean', ascending=False))"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 5 [cell {i}]: country salary agg sort_values")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 6: order_v groupby median().sort_values() inside loop
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "order_v = jobs.groupby(col)['salary_mid'].median().sort_values(ascending=False).index.tolist()" in src:
        new = src.replace(
            "order_v = jobs.groupby(col)['salary_mid'].median().sort_values(ascending=False).index.tolist()",
            "_ov: pd.Series = pd.Series(jobs.groupby(col)['salary_mid'].median())\n"
            "    order_v: list = _ov.sort_values(ascending=False).index.tolist()"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 6 [cell {i}]: order_v in loop groupby median().sort_values()")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 7: ct[condition].sort_values('year') — 3 loops in country trends
#   Replace: sub = ct[ct['country']==country_name].sort_values('year')
#   With:    sub: pd.DataFrame = pd.DataFrame(ct[ct['country']==country_name]).sort_values('year')
# ─────────────────────────────────────────────────────────────────────────
patched_ct = 0
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "sub = ct[ct['country']==country_name].sort_values('year')" in src:
        new = src.replace(
            "sub = ct[ct['country']==country_name].sort_values('year')",
            "sub: pd.DataFrame = pd.DataFrame(ct[ct['country']==country_name]).sort_values('year')"
        )
        set_src(c, new)
        fixes += 1
        patched_ct += 1
        print(f"  FIX 7 [cell {i}]: ct[filter].sort_values() explicit DataFrame (occurrence {patched_ct})")

# ─────────────────────────────────────────────────────────────────────────
# FIX 8: remote_flag groupby mean().mul(100) — replace .mul(100) with * 100
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "remote_year = jobs.groupby('posted_year')['remote_flag'].mean().mul(100)" in src:
        new = src
        new = new.replace(
            "remote_year = jobs.groupby('posted_year')['remote_flag'].mean().mul(100)",
            "_remote_year_s: pd.Series = pd.Series(jobs.groupby('posted_year')['remote_flag'].mean())\n"
            "remote_year: pd.Series = _remote_year_s * 100"
        )
        new = new.replace(
            "remote_country = jobs.groupby('country')['remote_flag'].mean().mul(100).sort_values(ascending=False)",
            "_remote_ctry_s: pd.Series = pd.Series(jobs.groupby('country')['remote_flag'].mean())\n"
            "remote_country: pd.Series = (_remote_ctry_s * 100).sort_values(ascending=False)"
        )
        new = new.replace(
            "remote_exp = jobs.groupby('experience_level')['remote_flag'].mean().mul(100).reindex(['Entry','Mid','Senior'])",
            "_remote_exp_s: pd.Series = pd.Series(jobs.groupby('experience_level')['remote_flag'].mean())\n"
            "remote_exp: pd.Series = (_remote_exp_s * 100).reindex(['Entry','Mid','Senior'])"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 8 [cell {i}]: remote_flag groupby .mul(100) -> * 100, explicit Series")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 9: subset['job_title'].value_counts().sort_values() in hist/proj loop
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "counts = subset['job_title'].value_counts().sort_values()" in src:
        new = src.replace(
            "counts = subset['job_title'].value_counts().sort_values()",
            "_vc: pd.Series = pd.Series(subset['job_title'].value_counts())\n"
            "    counts: pd.Series = _vc.sort_values()"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 9 [cell {i}]: subset value_counts().sort_values() explicit Series")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 10: city_counts value_counts() — already a Series, but pyright
#   needs: city_counts = pd.Series(jobs[...]['city'].value_counts()).head(20)
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "city_counts = jobs[jobs['city'] != 'Remote']['city'].value_counts().head(20)" in src:
        new = src.replace(
            "city_counts = jobs[jobs['city'] != 'Remote']['city'].value_counts().head(20)",
            "_city_vc: pd.Series = pd.Series(jobs[jobs['city'] != 'Remote']['city'].value_counts())\n"
            "city_counts: pd.Series = _city_vc.head(20)"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 10 [cell {i}]: city_counts value_counts() explicit Series")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 11: jobs_hist_ml.copy() → pd.DataFrame(jobs_hist_ml)
#   and strat_col / X_base chain — ML cell
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "jobs_hist_ml = jobs_ml[jobs_ml['period_type'] == 'Historical'].copy()" in src:
        new = src.replace(
            "jobs_hist_ml = jobs_ml[jobs_ml['period_type'] == 'Historical'].copy()",
            "jobs_hist_ml: pd.DataFrame = pd.DataFrame(jobs_ml[jobs_ml['period_type'] == 'Historical'])"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 11 [cell {i}]: jobs_hist_ml explicit pd.DataFrame cast")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 12: strat_col = jobs_hist_ml['experience_level'].values  → .to_numpy()
#   X_base = jobs_hist_ml['experience_level'].map(exp_map).values.reshape(-1,1)
#       → np.array(jobs_hist_ml['experience_level'].map(exp_map)).reshape(-1,1)
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "strat_col = jobs_hist_ml['experience_level'].values" in src:
        new = src.replace(
            "strat_col = jobs_hist_ml['experience_level'].values",
            "strat_col: np.ndarray = jobs_hist_ml['experience_level'].to_numpy()"
        )
        new = new.replace(
            "X_base = jobs_hist_ml['experience_level'].map(exp_map).values.reshape(-1,1)",
            "X_base: np.ndarray = np.array(jobs_hist_ml['experience_level'].map(exp_map).tolist(), dtype=float).reshape(-1, 1)"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 12 [cell {i}]: strat_col .to_numpy(), X_base np.array().reshape()")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 13: y_test_vals = best_model_result['y_test'].values  → .to_numpy()
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "y_test_vals  = best_model_result['y_test'].values" in src:
        new = src.replace(
            "y_test_vals  = best_model_result['y_test'].values",
            "y_test_vals: np.ndarray = np.array(best_model_result['y_test'])"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 13 [cell {i}]: y_test_vals .values -> np.array()")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 14: KMeans(n_init=10) — sklearn stub incorrectly types n_init as str
#   Add # type: ignore[call-arg] comment
# ─────────────────────────────────────────────────────────────────────────
patched_km = 0
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "KMeans(n_clusters=k, random_state=42, n_init=10)" in src or \
       "KMeans(n_clusters=best_k, random_state=42, n_init=10)" in src:
        new = src.replace(
            "KMeans(n_clusters=k, random_state=42, n_init=10)",
            "KMeans(n_clusters=k, random_state=42, n_init=10)  # type: ignore[call-arg]"
        ).replace(
            "KMeans(n_clusters=best_k, random_state=42, n_init=10)",
            "KMeans(n_clusters=best_k, random_state=42, n_init=10)  # type: ignore[call-arg]"
        )
        set_src(c, new)
        fixes += 1
        patched_km += 1
        print(f"  FIX 14 [cell {i}]: KMeans n_init=10 type: ignore (sklearn stub bug)")

# ─────────────────────────────────────────────────────────────────────────
# FIX 15: grp["salary_mid"].median() in key insights loop
#   pyright can't narrow grp from boolean index; use float() cast in f-string
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if "grp[\"salary_mid\"].mean():>9,.0f}  median=${grp[\"salary_mid\"].median():>9,.0f}" in src:
        new = src.replace(
            "print(f'   {exp:<8}: mean=${grp[\"salary_mid\"].mean():>9,.0f}  median=${grp[\"salary_mid\"].median():>9,.0f}')",
            "_mean_v = float(grp[\"salary_mid\"].mean())\n"
            "    _med_v  = float(grp[\"salary_mid\"].median())\n"
            "    print(f'   {exp:<8}: mean=${_mean_v:>9,.0f}  median=${_med_v:>9,.0f}')"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 15 [cell {i}]: salary mean/median explicit float() in f-string")
        break

# ─────────────────────────────────────────────────────────────────────────
# FIX 16: reindex on groupby result (.agg) for the stats table
#   print(jobs.groupby(...).agg([...]).round(0).reindex(order))
# ─────────────────────────────────────────────────────────────────────────
for i, c in enumerate(cells):
    if c["cell_type"] != "code":
        continue
    src = get_src(c)
    if ".agg(['mean','median','std']).round(0).reindex(order)" in src:
        new = src.replace(
            "print(jobs.groupby('experience_level')['salary_mid'].agg(['mean','median','std']).round(0).reindex(order))",
            "_sal_agg: pd.DataFrame = pd.DataFrame(jobs.groupby('experience_level')['salary_mid'].agg(['mean','median','std'])).round(0)\n"
            "print(_sal_agg.reindex(order))"
        )
        set_src(c, new)
        fixes += 1
        print(f"  FIX 16 [cell {i}]: salary agg stats .reindex(order) explicit DataFrame")
        break

print(f"\nTotal fixes applied: {fixes}")

# Save the notebook
NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Saved {NB_PATH} ({NB_PATH.stat().st_size // 1024} KB)")
