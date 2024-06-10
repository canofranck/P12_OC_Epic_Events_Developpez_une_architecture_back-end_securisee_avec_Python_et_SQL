from sqlalchemy import (
    Column,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    String,
)
from datetime import datetime


from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Relation with Users:
    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="contract")

    # Relation with Customers:

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    user: Mapped["Customer"] = relationship(back_populates="contract")

    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)
    is_signed = Column(Boolean, default=False, nullable=False)

    # Relation with Events one to one :
    events: Mapped["Event"] = relationship(
        back_populates="contract", uselist=False
    )

    def __init__(
        self,
        customer_id,
        manager_id,
        total_amount,
        remaining_amount,
        creation_date,
        is_signed=False,
    ):

        self.customer_id = customer_id
        self.manager_id = manager_id
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.creation_date = creation_date
        self.is_signed = is_signed

    def __str__(self):
        return (
            f"Contract ID: {self.id}, "
            f"Client ID: {self.customer_id}, "
            f"User ID: {self.manager_id}, "
            f"Total Amount: {self.total_amount}, "
            f"Remaining Amount: {self.remaining_amount}, "
            f"Creation Date: {self.creation_date}, "
            f"Status: {'Signed' if self.is_signed else 'Not Signed'}"
        )
