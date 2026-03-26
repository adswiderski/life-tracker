from pydantic import BaseModel
import datetime


class FitnessLogBase(BaseModel):
    date: datetime.date
    weight: float | None = None
    gym_done: int = 0
    steps: int | None = None
    cardio_minutes: int | None = None
    calories: int | None = None
    protein: float | None = None
    carbs: float | None = None
    fats: float | None = None
    salt: float | None = None
    notes: str | None = None


class FitnessLogCreate(FitnessLogBase):
    pass


class FitnessLogUpdate(BaseModel):
    date: datetime.date | None = None
    weight: float | None = None
    gym_done: int | None = None
    steps: int | None = None
    cardio_minutes: int | None = None
    calories: int | None = None
    protein: float | None = None
    carbs: float | None = None
    fats: float | None = None
    salt: float | None = None
    notes: str | None = None


class FitnessLogResponse(FitnessLogBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
