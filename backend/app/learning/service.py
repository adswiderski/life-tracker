# learning/service.py
import datetime as dt

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.learning.models import LearningGoal, LearningLog


async def get_goals_by_user(db: AsyncSession, user_id: int) -> list[LearningGoal]:
    result = await db.execute(
        select(LearningGoal)
        .where(LearningGoal.user_id == user_id)
        .order_by(LearningGoal.created_at.desc())
    )
    return list(result.scalars().all())


async def get_goal_by_id(
    db: AsyncSession, user_id: int, goal_id: int
) -> LearningGoal | None:
    result = await db.execute(
        select(LearningGoal).where(
            LearningGoal.id == goal_id,
            LearningGoal.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def create_goal(db: AsyncSession, user_id: int, data: dict) -> LearningGoal:
    goal = LearningGoal(user_id=user_id, **data)
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


async def update_goal(db: AsyncSession, goal: LearningGoal, data: dict) -> LearningGoal:
    for key, value in data.items():
        setattr(goal, key, value)
    await db.commit()
    await db.refresh(goal)
    return goal


async def delete_goal(db: AsyncSession, goal: LearningGoal) -> None:
    await db.delete(goal)
    await db.commit()


async def get_logs_by_goal(
    db: AsyncSession, user_id: int, goal_id: int
) -> list[LearningLog]:
    result = await db.execute(
        select(LearningLog)
        .where(
            LearningLog.goal_id == goal_id,
            LearningLog.user_id == user_id,
        )
        .order_by(LearningLog.date.desc())
    )
    return list(result.scalars().all())


async def get_log_by_date(
    db: AsyncSession, user_id: int, goal_id: int, date: dt.date
) -> LearningLog | None:
    result = await db.execute(
        select(LearningLog).where(
            LearningLog.goal_id == goal_id,
            LearningLog.user_id == user_id,
            LearningLog.date == date,
        )
    )
    return result.scalar_one_or_none()


async def create_log(
    db: AsyncSession, user_id: int, goal_id: int, data: dict
) -> LearningLog:
    log = LearningLog(user_id=user_id, goal_id=goal_id, **data)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


async def update_log(db: AsyncSession, log: LearningLog, data: dict) -> LearningLog:
    for key, value in data.items():
        setattr(log, key, value)
    await db.commit()
    await db.refresh(log)
    return log


async def delete_log(db: AsyncSession, log: LearningLog) -> None:
    await db.delete(log)
    await db.commit()


async def get_goal_progress(db: AsyncSession, user_id: int, goal_id: int) -> dict:
    result = await db.execute(
        select(
            func.sum(LearningLog.minutes).label("total_minutes"),
            func.sum(LearningLog.pages).label("total_pages"),
            func.sum(LearningLog.tasks).label("total_tasks"),
        ).where(
            LearningLog.goal_id == goal_id,
            LearningLog.user_id == user_id,
        )
    )
    row = result.one()
    return {
        "total_minutes": row.total_minutes or 0,
        "total_pages": row.total_pages or 0,
        "total_tasks": row.total_tasks or 0,
    }
