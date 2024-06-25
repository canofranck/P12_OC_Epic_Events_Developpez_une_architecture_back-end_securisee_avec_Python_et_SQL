from sqlalchemy import Column, String


from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name
