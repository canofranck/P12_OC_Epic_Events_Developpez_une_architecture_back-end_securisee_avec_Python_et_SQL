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
from models.user import User


class Contract(Base):
    """
    Represents a contract in the database.

    Attributes:
    -----------
    id : int
        Unique identifier for the contract.
    manager_id : int
        Foreign key referencing the user who manages the contract.
    user : User
        The user associated with the contract.
    customer_id : int
        Foreign key referencing the customer.
    customer : Customer
        The customer associated with the contract.
    total_amount : float
        Total amount of the contract.
    remaining_amount : float
        Remaining amount to be paid on the contract.
    creation_date : datetime
        The date and time when the contract was created.
    is_signed : bool
        Indicates whether the contract is signed.
    event : Event
        The event associated with the contract (one-to-one relationship).
    """

    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Relation with Users:
    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="contracts")

    # Relation with Customers:

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship(back_populates="contracts")

    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=datetime.now, nullable=False)
    is_signed = Column(Boolean, default=False, nullable=False)

    # Relation with Events one to one :
    event: Mapped["Event"] = relationship(
        back_populates="contract", uselist=False
    )

    def __init__(
        self,
        total_amount,
        remaining_amount,
        is_signed=False,
        user=None,
        customer=None,
    ):
        """
        Initializes a new Contract instance.

        Parameters:
        -----------
        total_amount : float
            The total amount of the contract.
        remaining_amount : float
            The remaining amount to be paid.
        is_signed : bool, optional
            Indicates whether the contract is signed (default is False).
        user : User, optional
            The user associated with the contract (default is None).
        customer : Customer, optional
            The customer associated with the contract (default is None).
        """
        self.total_amount = total_amount
        self.remaining_amount = remaining_amount
        self.creation_date = datetime.now()
        self.is_signed = is_signed
        self.user = user
        self.customer = customer

    def __str__(self):
        """
        Returns a string representation of the contract.

        Returns:
        --------
        str
            A string containing the contract details.
        """
        return (
            f"Contract ID: {self.id}, "
            f"Client ID: {self.customer_id}, "
            f"User ID: {self.manager_id}, "
            f"Total Amount: {self.total_amount}, "
            f"Remaining Amount: {self.remaining_amount}, "
            f"Creation Date: {self.creation_date}, "
            f"Status: {'Signed' if self.is_signed else 'Not Signed'}"
        )
