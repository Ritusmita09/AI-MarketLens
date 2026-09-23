"""fix_sub_redecl.py — remove repeated sub: pd.DataFrame type annotation (reportRedeclaration)"""
import json, pathlib

NB_PATH = pathlib.Path("submission/Ritusmita_AI_MarketLens.ipynb")
nb = json.loads(NB_PATH.read_text(encoding="utf-8"))

fixed = 0
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    if "sub: pd.DataFrame = pd.DataFrame(" in src:
        new = src.replace(
            "sub: pd.DataFrame = pd.DataFrame(ct[ct['country']==country_name]).sort_values('year')",
            "sub = pd.DataFrame(ct[ct['country']==country_name]).sort_values('year')"
        )
        c["source"] = new.splitlines(keepends=True)
        fixed += 1
        print(f"  Fixed sub: pd.DataFrame annotation in cell")

print(f"Total occurrences fixed: {fixed}")
NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("Saved.")
