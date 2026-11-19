import uuid
from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    cut_off_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

    activities: Mapped[list["Activity"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint("btrim(name) <> ''", name="chk_project_name_not_empty"),
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    bac: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    planned_progress: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    actual_progress: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    actual_cost: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

    project: Mapped[Project] = relationship(back_populates="activities")

    __table_args__ = (
        CheckConstraint("bac >= 0", name="chk_activity_bac_non_negative"),
        CheckConstraint("planned_progress between 0 and 100", name="chk_activity_planned_progress_range"),
        CheckConstraint("actual_progress between 0 and 100", name="chk_activity_actual_progress_range"),
        CheckConstraint("actual_cost >= 0", name="chk_activity_actual_cost_non_negative"),
    )
