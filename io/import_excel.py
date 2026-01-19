import pandas as pd
import yaml
from sqlalchemy.orm import Session

from core.model import Vehicle
from core.matcher import match_vehicle
from core.sync import sync_vehicle


def load_mapping(path="config/input_mapping.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def transform_value(value, transforms):
    for t in transforms or []:
        if value is None:
            return None

        if t == "strip":
            value = str(value).strip()
        elif t == "uppercase":
            value = str(value).upper()
        elif t == "lowercase":
            value = str(value).lower()
        elif t == "date":
            value = pd.to_datetime(value, dayfirst=True).date()
    return value


def import_excel(
    session: Session,
    excel_path: str,
    source: str,
):
    mapping = load_mapping()
    df = pd.read_excel(excel_path)

    for _, row in df.iterrows():
        incoming_data = {}

        for col, cfg in mapping["columns"].items():
            raw_value = row.get(col)
            value = transform_value(raw_value, cfg.get("transform"))
            incoming_data[cfg["field"]] = value

        vehicles = session.query(Vehicle).all()
        matched_vehicle = None

        for vehicle in vehicles:
            if match_vehicle(
                vehicle,
                incoming_data.get("reservation_number"),
                incoming_data.get("vin"),
            ):
                matched_vehicle = vehicle
                break

        if matched_vehicle:
            sync_vehicle(
                matched_vehicle,
                incoming_data,
                source=source,
            )
        else:
            new_vehicle = Vehicle(**incoming_data)
            new_vehicle.source_file = source
            session.add(new_vehicle)

    session.commit()
