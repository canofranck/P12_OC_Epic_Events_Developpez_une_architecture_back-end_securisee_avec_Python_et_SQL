from sqlalchemy.orm import relationship
from sqlalchemy import (
    CHAR,
    VARCHAR,
    Column,
    Integer,
    String,
    ForeignKey,
    UUID,
    DateTime,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from models.base import Base
from typing import List


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Relation with User:
    sales_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="customers")

    # Relation with Contract
    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, index=True)
    phone_number = Column(String(20), unique=False, index=True)
    compagny_name = Column(String(100), unique=False, index=True)
    creation_date = Column(DateTime, default=datetime.now)
    last_contact_date = Column(DateTime, default=datetime.now)

    def __init__(
        self,
        first_name,
        last_name,
        email,
        phone_number,
        compagny_name,
        sales_id,
    ):

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.compagny_name = compagny_name

        self.sales_id = sales_id

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
