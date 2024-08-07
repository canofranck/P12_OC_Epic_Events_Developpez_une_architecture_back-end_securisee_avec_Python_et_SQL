import os
from typing import List
import bcrypt
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import Base


class User(Base):
    """
    Represents a user in the database.

    Attributes:
    -----------
    id : int
        Unique identifier for the user.
    username : str
        The username of the user.
    password : str
        The hashed password of the user.
    full_name : str
        The full name of the user.
    email : str
        The email address of the user.
    phone_number : str
        The phone number of the user.
    role_id : int
        Foreign key referencing the role of the user.
    role : Role
        The role associated with the user.
    contracts : List[Contract]
        List of contracts associated with the user.
    customers : List[Customer]
        List of customers managed by the user.
    events : List[Event]
        List of events managed by the user.
    """

    salt = os.getenv("salt")
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    customers: Mapped[List["Customer"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    events: Mapped[List["Event"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        username,
        full_name,
        email,
        phone_number,
        role_id,
        password=None,
        salt=salt,
    ):
        """
        Initializes a new User instance.

        Parameters:
        -----------
        username : str
            The username of the user.
        full_name : str
            The full name of the user.
        email : str
            The email address of the user.
        phone_number : str
            The phone number of the user.
        role_id : int
            The role identifier for the user.
        password : str, optional
            The plain text password of the user (default is None).
        """

        self.username = username
        self.full_name = full_name
        self.role_id = role_id
        self.email = email
        self.phone_number = phone_number
        self.salt = os.getenv("salt")
        if password:
            self.set_password(password)

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
        --------
        str
            A string containing the user details.
        """
        return (
            f"User Name: {self.username} "
            f"Full Name: {self.full_name} "
            f"Email: {self.email} "
            f"Role: {self.role} "
        )

    def set_password(self, password: str) -> None:
        """
        Sets the password for the user by hashing it.

        Parameters:
        -----------
        password : str
            The plain text password to be hashed and set for the user.
        """
        salt = os.getenv("salt")
        bytes = password.encode("utf-8")
        hash_password = bcrypt.hashpw(bytes, self.salt.encode("utf-8"))
        self.password = hash_password.decode("utf-8")

    def is_password_correct(self, input_password):
        """
        Checks if the provided password is correct for the user.

        This method hashes the input password using the salt and compares it to the user's password stored in the database.
        If the passwords match, it returns True. Otherwise, it returns False.

        Returns:
            is_correct: A boolean indicating whether the password is correct.
        """
        salt = os.getenv("salt")
        input_bytes = input_password.encode("utf-8")
        hash_input_password = bcrypt.hashpw(input_bytes, salt.encode("utf-8"))
        is_correct = hash_input_password == self.password.encode("utf-8")
        return is_correct
