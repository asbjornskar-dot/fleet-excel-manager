import pandas as pd
import yaml
from sqlalchemy.orm import Session
from core.model import Vehicle


def load_export_mapping(path="config/export_mapping.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def export_excels(
    session: Session,
    output_dir: str = "exports",
):
    mapping = load_export_mapping()
    exports = mapping["exports"]

    output_path = pd.Path(output_dir) if hasattr(pd, "Path") else None

    vehicles = session.query(Vehicle).all()

    for export_key, cfg in exports.items():
        rows = []
        for v in vehicles:
            row = {}
            for field in cfg["columns"]:
                row[field] = getattr(v, field)
            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_excel(cfg["filename"], index=False)
