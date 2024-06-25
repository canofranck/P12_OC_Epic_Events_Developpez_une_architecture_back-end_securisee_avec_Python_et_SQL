from typing import List
import uuid
import bcrypt
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import (
    CHAR,
    VARCHAR,
    Column,
    ForeignKey,
    Integer,
    String,
    UUID,
    Enum,
)
import enum


from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from models.base import Base
import logging


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

salt = b"$2b$12$QhTfGmCB1FrbuySv8Op4IO"


class UserPermission:
    pass


# class UserRole(enum.Enum):
#     MANAGER = 1
#     SALES = 2
#     SUPPORT = 3
#     ADMIN = 4

#     def __str__(self):
#         return self.name


class User(Base):

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
    ):
        if password:
            self.set_password(password)

        self.username = username
        self.full_name = full_name
        self.role_id = role_id
        self.email = email
        self.phone_number = phone_number

    def __str__(self):
        return (
            f"User Name: {self.username} "
            f"Full Name: {self.full_name} "
            f"Email: {self.email} "
            f"Role: {self.role} "
        )

    def set_password(self, password: str) -> None:
        bytes = password.encode("utf-8")
        hash_password = bcrypt.hashpw(bytes, salt)
        self.password = hash_password.decode("utf-8")
