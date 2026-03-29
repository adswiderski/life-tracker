import datetime as dt
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.fitness.models import FitnessLog


async def get_logs_by_user(db: AsyncSession, user_id: int) -> list[FitnessLog]:
    result = await db.execute(
        select(FitnessLog)
        .where(FitnessLog.user_id == user_id)
        .order_by(FitnessLog.date.desc())
    )
    return list(result.scalars().all())


async def get_log_by_date(
    db: AsyncSession, user_id: int, date: dt.date
) -> FitnessLog | None:
    result = await db.execute(
        select(FitnessLog).where(
            FitnessLog.user_id == user_id,
            FitnessLog.date == date,
        )
    )
    return result.scalar_one_or_none()


async def create_log(
    db: AsyncSession, user_id: int, data: dict[str, Any]
) -> FitnessLog:
    log = FitnessLog(user_id=user_id, **data)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def update_log(
    db: AsyncSession, log: FitnessLog, data: dict[str, Any]
) -> FitnessLog:
    for key, value in data.items():
        setattr(log, key, value)
    await db.commit()
    await db.refresh(log)
    return log


async def delete_log(db: AsyncSession, log: FitnessLog) -> None:
    await db.delete(log)
    await db.commit()
