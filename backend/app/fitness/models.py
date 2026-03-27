from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class FitnessLog(Base):
    __tablename__ = "fitness_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

    weight: Mapped[float | None] = mapped_column(nullable=True)

    gym_done: Mapped[int] = mapped_column(default=0)
    steps: Mapped[int | None] = mapped_column(nullable=True)
    cardio_minutes: Mapped[int | None] = mapped_column(nullable=True)

    calories: Mapped[int | None] = mapped_column(nullable=True)
    protein: Mapped[float | None] = mapped_column(nullable=True)
    carbs: Mapped[float | None] = mapped_column(nullable=True)
    fats: Mapped[float | None] = mapped_column(nullable=True)
    salt: Mapped[float | None] = mapped_column(nullable=True)

    notes: Mapped[str | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
