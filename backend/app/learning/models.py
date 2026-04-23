# learning/models.py
import datetime as dt
from enum import Enum

from sqlalchemy import DateTime, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class GoalStatus(str, Enum):
    active = "active"
    completed = "completed"
    abandoned = "abandoned"


class LearningGoal(Base):
    __tablename__ = "learning_goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column()
    status: Mapped[GoalStatus] = mapped_column(default=GoalStatus.active)

    target_minutes: Mapped[int | None] = mapped_column()
    target_pages: Mapped[int | None] = mapped_column()
    target_tasks: Mapped[int | None] = mapped_column()

    started_at: Mapped[dt.date] = mapped_column(Date, nullable=False)
    deadline: Mapped[dt.date | None] = mapped_column(Date)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.UTC),
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.UTC),
        onupdate=lambda: dt.datetime.now(dt.UTC),
    )

    logs: Mapped[list["LearningLog"]] = relationship(back_populates="goal")


class LearningLog(Base):
    __tablename__ = "learning_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    goal_id: Mapped[int] = mapped_column(
        ForeignKey("learning_goals.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[dt.date] = mapped_column(Date, nullable=False)

    minutes: Mapped[int | None] = mapped_column()
    pages: Mapped[int | None] = mapped_column()
    tasks: Mapped[int | None] = mapped_column()
    notes: Mapped[str | None] = mapped_column()

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.UTC),
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.UTC),
        onupdate=lambda: dt.datetime.now(dt.UTC),
    )

    goal: Mapped["LearningGoal"] = relationship(back_populates="logs")
