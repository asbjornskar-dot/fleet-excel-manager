from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    DateTime,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


def generate_system_id() -> str:
    """
    Internal permanent ID.

    Used mainly for:
    - Stock vehicles
    - Vehicles without reservation number
    - Vehicles without customer

    This ID is NEVER edited by users and is the final fallback identity.
    """
    return str(uuid.uuid4())


class Vehicle(Base):
    __tablename__ = "vehicles"

    # --------------------------------------------------
    # Internal identity (always present)
    # --------------------------------------------------
    system_id = Column(
        String,
        primary_key=True,
        default=generate_system_id
    )

    # --------------------------------------------------
    # Business identifiers (priority order)
    #
    # 1. reservation_number  (normal sales flow)
    # 2. vin                 (often arrives later)
    # 3. system_id           (stock / fallback)
    # --------------------------------------------------
    reservation_number = Column(String, nullable=True)
    vin = Column(String, nullable=True)

    # --------------------------------------------------
    # Customer information (may be missing)
    # --------------------------------------------------
    customer_name = Column(String, nullable=True)

    # --------------------------------------------------
    # Vehicle details
    # --------------------------------------------------
    model = Column(String, nullable=True)
    color = Column(String, nullable=True)
    winter_tires = Column(Boolean, nullable=True)

    # --------------------------------------------------
    # Dates
    # --------------------------------------------------
    eta = Column(Date, nullable=True)
    delivery_date = Column(Date, nullable=True)
    delivery_time = Column(String, nullable=True)

    # --------------------------------------------------
    # Process / preparation
    # --------------------------------------------------
    preparation_color_code = Column(String, nullable=True)

    # --------------------------------------------------
    # Comments (user editable)
    # --------------------------------------------------
    comment_1 = Column(Text, nullable=True)
    comment_2 = Column(Text, nullable=True)
    comment_3 = Column(Text, nullable=True)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------
    last_updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    source_file = Column(
        String,
        nullable=True,
        doc="Which file last updated this row (admin / full / delivery)"
    )

    def __repr__(self):
        return (
            f"<Vehicle("
            f"system_id={self.system_id}, "
            f"reservation={self.reservation_number}, "
            f"vin={self.vin})>"
        )
