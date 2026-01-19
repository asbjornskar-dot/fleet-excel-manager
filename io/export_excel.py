import pandas as pd
import yaml
from io import BytesIO
from sqlalchemy.orm import Session
from core.model import Vehicle


def load_export_mapping(path="config/export_mapping.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def export_excels(session: Session):
    mapping = load_export_mapping()
    exports = mapping["exports"]

    vehicles = session.query(Vehicle).all()
    output_files = {}

    for export_key, cfg in exports.items():
        rows = []

        for v in vehicles:
            row = {}
            for field in cfg["columns"]:
                row[field] = getattr(v, field)
            rows.append(row)

        df = pd.DataFrame(rows)

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        output_files[cfg["filename"]] = buffer

    return output_files
