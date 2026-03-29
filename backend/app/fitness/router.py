import datetime as dt

from fastapi import APIRouter, HTTPException, status

from app.auth.service import get_user_by_email
from app.core.dependencies import CurrentUserEmail, DBSession
from app.fitness import schemas, service as fitness_service

router = APIRouter()


@router.get("/logs", response_model=list[schemas.FitnessLogResponse])
async def get_logs(current_user_email: CurrentUserEmail, db: DBSession):
    user = await get_user_by_email(db, current_user_email)
    return await fitness_service.get_logs_by_user(db, user.id)


@router.get("/logs/{log_date}", response_model=schemas.FitnessLogResponse)
async def get_log(
    log_date: dt.date, current_user_email: CurrentUserEmail, db: DBSession
):
    user = await get_user_by_email(db, current_user_email)
    log = await fitness_service.get_log_by_date(db, user.id, log_date)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return log


@router.post(
    "/logs",
    response_model=schemas.FitnessLogResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_log(
    payload: schemas.FitnessLogCreate,
    current_user_email: CurrentUserEmail,
    db: DBSession,
):
    user = await get_user_by_email(db, current_user_email)
    existing = await fitness_service.get_log_by_date(db, user.id, payload.date)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot create log for this date - it already exists.",
        )
    return await fitness_service.create_log(db, user.id, payload.model_dump())


@router.patch("/logs/{log_date}", response_model=schemas.FitnessLogResponse)
async def update_log(
    log_date: dt.date,
    payload: schemas.FitnessLogUpdate,
    current_user_email: CurrentUserEmail,
    db: DBSession,
):
    user = await get_user_by_email(db, current_user_email)
    log = await fitness_service.get_log_by_date(db, user.id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot update log for this date - it doesn't exist",
        )
    await fitness_service.update_log(db, log, payload.model_dump(exclude_unset=True))


@router.delete("/logs/{log_date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(
    log_date: dt.date,
    current_user_email: CurrentUserEmail,
    db: DBSession,
):
    user = await get_user_by_email(db, current_user_email)
    log = await fitness_service.get_log_by_date(db, user.id, log_date)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot delete log for this date - it doesn't exist",
        )
    await fitness_service.delete_log(db, log)
