from datetime import datetime
from typing import Optional
from core.model import Vehicle


SOURCE_PRIORITY = {
    "admin": 3,
    "full": 2,
    "delivery": 1,
}


def should_update(
    current_value,
    incoming_value,
) -> bool:
    """
    Determines whether a field should be updated.

    Rules:
    - None or empty incoming value -> DO NOT overwrite
    - Different non-empty value -> update
    """
    if incoming_value is None:
        return False

    if isinstance(incoming_value, str) and incoming_value.strip() == "":
        return False

    return incoming_value != current_value


def apply_field(
    vehicle: Vehicle,
    field_name: str,
    incoming_value,
):
    setattr(vehicle, field_name, incoming_value)


def sync_vehicle(
    vehicle: Vehicle,
    incoming_data: dict,
    source: str,
) -> Vehicle:
    """
    Syncs incoming data into an existing Vehicle record.

    Source priority:
    admin > full > delivery
    """

    if source not in SOURCE_PRIORITY:
        raise ValueError(f"Unknown source: {source}")

    incoming_priority = SOURCE_PRIORITY[source]

    # If record has a previous source, check priority
    if vehicle.source_file:
        current_priority = SOURCE_PRIORITY.get(vehicle.source_file, 0)
        if incoming_priority < current_priority:
            # Lower priority source -> only allow comment + prep color updates
            allowed_fields = {
                "comment_1",
                "comment_2",
                "comment_3",
                "preparation_color_code",
            }
        else:
            allowed_fields = incoming_data.keys()
    else:
        allowed_fields = incoming_data.keys()

    for field, value in incoming_data.items():
        if field not in allowed_fields:
            continue

        current_value = getattr(vehicle, field)

        if should_update(current_value, value):
            apply_field(vehicle, field, value)

    vehicle.last_updated = datetime.utcnow()
    vehicle.source_file = source

    return vehicle
