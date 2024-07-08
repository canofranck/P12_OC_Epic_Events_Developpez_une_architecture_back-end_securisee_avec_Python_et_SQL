from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime

from models.base import Base


class Event(Base):

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
        # support_id,
        # contract_id,
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
        # self.support_id = support_id
        # self.contract_id = contract_id

    def __str__(self):
        return f"Event {self.id} - Name: {self.event_name} - Start: {self.start_date} - End: {self.end_date} - Location: {self.location} - Attendees: {self.nb_attendees}"
