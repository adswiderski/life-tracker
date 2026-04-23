# learning/router.py
import datetime as dt

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUserId, DBSession
from app.learning import schemas, service
from app.learning.models import LearningGoal, LearningLog

router = APIRouter()


# ── Goals ─────────────────────────────────────────────────────


@router.get("/goals", response_model=list[schemas.LearningGoalResponse])
async def get_goals(
    current_user_id: CurrentUserId, db: DBSession
) -> list[LearningGoal]:
    return await service.get_goals_by_user(db, current_user_id)


@router.get("/goals/{goal_id}", response_model=schemas.LearningGoalResponse)
async def get_goal(
    goal_id: int, current_user_id: CurrentUserId, db: DBSession
) -> LearningGoal:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    return goal


@router.post(
    "/goals",
    response_model=schemas.LearningGoalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_goal(
    payload: schemas.LearningGoalCreate, current_user_id: CurrentUserId, db: DBSession
) -> LearningGoal:
    return await service.create_goal(db, current_user_id, payload.model_dump())


@router.patch("/goals/{goal_id}", response_model=schemas.LearningGoalResponse)
async def update_goal(
    goal_id: int,
    payload: schemas.LearningGoalUpdate,
    current_user_id: CurrentUserId,
    db: DBSession,
) -> LearningGoal:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    return await service.update_goal(db, goal, payload.model_dump(exclude_unset=True))


@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int, current_user_id: CurrentUserId, db: DBSession
) -> None:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    await service.delete_goal(db, goal)


# ── Logs ──────────────────────────────────────────────────────


@router.get("/goals/{goal_id}/logs", response_model=list[schemas.LearningLogResponse])
async def get_logs(
    goal_id: int, current_user_id: CurrentUserId, db: DBSession
) -> list[LearningLog]:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    return await service.get_logs_by_goal(db, current_user_id, goal_id)


@router.post(
    "/goals/{goal_id}/logs",
    response_model=schemas.LearningLogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_log(
    goal_id: int,
    payload: schemas.LearningLogCreate,
    current_user_id: CurrentUserId,
    db: DBSession,
) -> LearningLog:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    if existing := await service.get_log_by_date(
        db, current_user_id, goal_id, payload.date
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Log for this date already exists",
        )
    return await service.create_log(db, current_user_id, goal_id, payload.model_dump())


@router.patch(
    "/goals/{goal_id}/logs/{log_date}", response_model=schemas.LearningLogResponse
)
async def update_log(
    goal_id: int,
    log_date: dt.date,
    payload: schemas.LearningLogUpdate,
    current_user_id: CurrentUserId,
    db: DBSession,
) -> LearningLog:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    log = await service.get_log_by_date(db, current_user_id, goal_id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
        )
    return await service.update_log(db, log, payload.model_dump(exclude_unset=True))


@router.delete(
    "/goals/{goal_id}/logs/{log_date}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_log(
    goal_id: int,
    log_date: dt.date,
    current_user_id: CurrentUserId,
    db: DBSession,
) -> None:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    log = await service.get_log_by_date(db, current_user_id, goal_id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
        )
    await service.delete_log(db, log)


@router.get("/goals/{goal_id}/progress", response_model=dict)
async def get_progress(
    goal_id: int, current_user_id: CurrentUserId, db: DBSession
) -> dict:
    goal = await service.get_goal_by_id(db, current_user_id, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )
    progress = await service.get_goal_progress(db, current_user_id, goal_id)
    return {
        "goal_id": goal_id,
        "target_minutes": goal.target_minutes,
        "target_pages": goal.target_pages,
        "target_tasks": goal.target_tasks,
        **progress,
    }
