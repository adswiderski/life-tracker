import datetime as dt

from pydantic import BaseModel, ConfigDict


class FitnessLogBase(BaseModel):
    date: dt.date
    weight: float | None = None
    gym_done: bool = False
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
    date: dt.date | None = None
    weight: float | None = None
    gym_done: bool | None = None
    steps: int | None = None
    cardio_minutes: int | None = None
    calories: int | None = None
    protein: float | None = None
    carbs: float | None = None
    fats: float | None = None
    salt: float | None = None
    notes: str | None = None


class FitnessLogResponse(FitnessLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: dt.datetime
    updated_at: dt.datetime
