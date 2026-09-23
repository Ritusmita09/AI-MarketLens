import json, uuid
from pathlib import Path

nb_path = Path("notebooks/AI_MarketLens_Master.ipynb")
nb = json.loads(nb_path.read_text(encoding="utf-8"))

# Add cell ids to all cells (required by newer nbformat)
for cell in nb["cells"]:
    if "id" not in cell:
        cell["id"] = str(uuid.uuid4())[:8]

nb_path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"Added ids. Total cells: {len(nb['cells'])}")
