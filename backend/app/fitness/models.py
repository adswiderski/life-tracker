from datetime import datetime, date as date_, UTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class FitnessLog(Base):
    __tablename__ = "fitness_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[date_] = mapped_column()

    weight: Mapped[float | None] = mapped_column()

    gym_done: Mapped[bool] = mapped_column()
    steps: Mapped[int | None] = mapped_column()
    cardio_minutes: Mapped[int | None] = mapped_column()

    calories: Mapped[int | None] = mapped_column()
    protein: Mapped[float | None] = mapped_column()
    carbs: Mapped[float | None] = mapped_column()
    fats: Mapped[float | None] = mapped_column()
    salt: Mapped[float | None] = mapped_column()

    notes: Mapped[str | None] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
