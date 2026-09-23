"""fix_map.py — fix the remaining 1 pyright error in the notebook"""
import json, pathlib
nb = json.loads(pathlib.Path("submission/Ritusmita_AI_MarketLens.ipynb").read_text(encoding="utf-8"))
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    needle = "np.array(jobs_hist_ml['experience_level'].map(pd.Series(exp_map)).tolist(), dtype=float)"
    if needle in src:
        replacement = "np.array([exp_map[v] for v in jobs_hist_ml['experience_level'].tolist()], dtype=float)"
        new = src.replace(needle, replacement)
        c["source"] = new.splitlines(keepends=True)
        print("Fixed: map(pd.Series(dict)) -> list comprehension")
        break
pathlib.Path("submission/Ritusmita_AI_MarketLens.ipynb").write_text(
    json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8"
)
print("Saved.")
