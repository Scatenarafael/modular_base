import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.settings.base import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    company_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"))

    number_of_cooldown_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user_company_roles = relationship("UserCompanyRole", back_populates="role")

    company = relationship("Company", back_populates="roles")
    work_days = relationship("WorkDay", back_populates="role", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<Role(id='{self.id}', name='{self.name}')>"
