import datetime as dt

from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUserId, DBSession
from app.fitness import schemas, service
from app.fitness.models import FitnessLog

router = APIRouter()


@router.get("/logs", response_model=list[schemas.FitnessLogResponse])
async def get_logs(current_user_id: CurrentUserId, db: DBSession) -> list[FitnessLog]:
    return await service.get_logs_by_user(db, current_user_id)


@router.get("/logs/{log_date}", response_model=schemas.FitnessLogResponse)
async def get_log(
    log_date: dt.date, current_user_id: CurrentUserId, db: DBSession
) -> FitnessLog:
    log = await service.get_log_by_date(db, current_user_id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
        )
    return log


@router.post(
    "/logs",
    response_model=schemas.FitnessLogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_log(
    payload: schemas.FitnessLogCreate, current_user_id: CurrentUserId, db: DBSession
) -> FitnessLog:
    if await service.get_log_by_date(db, current_user_id, payload.date):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Log for this date already exists",
        )
    return await service.create_log(db, current_user_id, payload.model_dump())


@router.patch("/logs/{log_date}", response_model=schemas.FitnessLogResponse)
async def update_log(
    log_date: dt.date,
    payload: schemas.FitnessLogUpdate,
    current_user_id: CurrentUserId,
    db: DBSession,
) -> FitnessLog:
    log = await service.get_log_by_date(db, current_user_id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
        )
    return await service.update_log(db, log, payload.model_dump(exclude_unset=True))


@router.delete("/logs/{log_date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(log_date: dt.date, current_user_id: CurrentUserId, db: DBSession):
    log = await service.get_log_by_date(db, current_user_id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Log not found"
        )
    await service.delete_log(db, log)
