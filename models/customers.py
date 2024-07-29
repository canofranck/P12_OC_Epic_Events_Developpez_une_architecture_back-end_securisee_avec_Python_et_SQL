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
    """
    Représente un client dans la base de données.

    Attributs:
    ----------
    id : int
        Identifiant unique du client.
    sales_id : int
        Clé étrangère référencant l'utilisateur responsable des ventes pour ce client.
    user : User
        L'utilisateur associé au client.
    contracts : List[Contract]
        Liste des contrats associés au client.
    first_name : str
        Prénom du client.
    last_name : str
        Nom de famille du client.
    email : str
        Adresse e-mail du client.
    phone_number : str
        Numéro de téléphone du client.
    compagny_name : str
        Nom de la société du client.
    creation_date : datetime
        Date et heure de création de l'enregistrement du client.
    last_contact_date : datetime
        Date et heure du dernier contact avec le client.
    """

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
        """
        Initialise une nouvelle instance de Customer.

        Paramètres:
        -----------
        first_name : str
            Prénom du client.
        last_name : str
            Nom de famille du client.
        email : str
            Adresse e-mail du client.
        phone_number : str
            Numéro de téléphone du client.
        compagny_name : str
            Nom de la société du client.
        sales_id : int
            Identifiant de l'utilisateur responsable des ventes pour ce client.
        """

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.compagny_name = compagny_name

        self.sales_id = sales_id

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères du client.

        Returns:
        --------
        str
            Une chaîne contenant les détails du client.
        """
        return f"{self.first_name} {self.last_name} ({self.email})"
