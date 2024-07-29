from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime

from models.base import Base


class Event(Base):
    """
    Represents an event in the database.

    Attributes:
    -----------
    id : int
        Unique identifier for the event.
    support_id : int
        Foreign key referencing the support user associated with the event.
    user : User
        The support user associated with the event.
    contract_id : int
        Foreign key referencing the contract associated with the event.
    contract : Contract
        The contract associated with the event.
    event_name : str
        The name of the event.
    customer_name : str
        The name of the customer hosting the event.
    start_date : datetime
        The start date and time of the event.
    end_date : datetime
        The end date and time of the event.
    location : str
        The location where the event is held.
    nb_attendees : int
        The number of attendees expected at the event.
    notes : str
        Additional notes or details about the event.
    """

    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Relation with Users:
    support_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="events")

    # relation with Contracts one to one :
    contract_id: Mapped[int] = mapped_column(
        ForeignKey("contracts.id"), unique=True
    )
    contract: Mapped["Contract"] = relationship(back_populates="event")

    event_name = Column(String(50), unique=True, index=True)
    customer_name = Column(String(50), unique=True, index=True)
    # customer_contact = Column(String(50), unique=False, index=True)
    start_date = Column(DateTime, unique=False, index=True)
    end_date = Column(DateTime, unique=False, index=True)
    location = Column(String(50), unique=False, index=True)
    nb_attendees = Column(Integer, unique=False, index=False)
    notes = Column(String(200), unique=False, index=False)

    def __init__(
        self,
        event_name,
        customer_name,
        customer_contact,
        start_date,
        end_date,
        location,
        nb_attendees,
        notes,
        user=None,
        contract=None,
    ):
        """
        Initializes a new Event instance.

        Parameters:
        -----------
        event_name : str
            The name of the event.
        customer_name : str
            The name of the customer hosting the event.
        customer_contact : str
            The contact information of the customer.
        start_date : datetime
            The start date and time of the event.
        end_date : datetime
            The end date and time of the event.
        location : str
            The location where the event is held.
        nb_attendees : int
            The number of attendees expected at the event.
        notes : str
            Additional notes or details about the event.
        user : User, optional
            The support user associated with the event (default is None).
        contract : Contract, optional
            The contract associated with the event (default is None).
        """

        self.event_name = event_name
        self.customer_name = customer_name
        self.customer_contact = customer_contact
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.nb_attendees = nb_attendees
        self.notes = notes
        self.user = user
        self.contract = contract

    def __str__(self):
        """
        Returns a string representation of the event.

        Returns:
        --------
        str
            A string containing the event details.
        """
        return f"Event {self.id} - Name: {self.event_name} - Start: {self.start_date} - End: {self.end_date} - Location: {self.location} - Attendees: {self.nb_attendees}"
