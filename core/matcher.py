from typing import Optional
from core.model import Vehicle


def match_vehicle(
    db_vehicle: Vehicle,
    reservation_number: Optional[str],
    vin: Optional[str],
) -> bool:
    """
    Determines whether an incoming row represents the same vehicle
    as an existing database record.

    Matching priority:
    1. Reservation number (primary business identity)
    2. VIN / chassis number
    3. Otherwise: no match
    """

    # 1️⃣ Reservation number match (highest priority)
    if reservation_number:
        if (
            db_vehicle.reservation_number
            and db_vehicle.reservation_number == reservation_number
        ):
            return True

    # 2️⃣ VIN match (secondary)
    if vin:
        if db_vehicle.vin and db_vehicle.vin == vin:
            return True

    # 3️⃣ No reliable match
    return False
