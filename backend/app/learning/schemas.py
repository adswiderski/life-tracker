# learning/schemas.py
import datetime as dt
from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator


class GoalStatus(str, Enum):
    active = "active"
    completed = "completed"
    abandoned = "abandoned"


class LearningGoalBase(BaseModel):
    name: str
    description: str | None = None
    target_minutes: int | None = None
    target_pages: int | None = None
    target_tasks: int | None = None
    started_at: dt.date
    deadline: dt.date | None = None

    @model_validator(mode="after")
    def at_least_one_target(self) -> "LearningGoalBase":
        if not any([self.target_minutes, self.target_pages, self.target_tasks]):
            raise ValueError(
                "At least one of target_minutes, target_pages, or target_tasks must be provided"
            )
        return self


class LearningGoalCreate(LearningGoalBase):
    pass


class LearningGoalUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: GoalStatus | None = None
    target_minutes: int | None = None
    target_pages: int | None = None
    target_tasks: int | None = None
    deadline: dt.date | None = None


class LearningGoalResponse(LearningGoalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: GoalStatus
    created_at: dt.datetime
    updated_at: dt.datetime


class LearningLogBase(BaseModel):
    date: dt.date
    minutes: int | None = None
    pages: int | None = None
    tasks: int | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def at_least_one_metric(self) -> "LearningLogBase":
        if not any([self.minutes, self.pages, self.tasks]):
            raise ValueError(
                "At least one of minutes, pages, or tasks must be provided"
            )
        return self


class LearningLogCreate(LearningLogBase):
    pass


class LearningLogUpdate(BaseModel):
    date: dt.date | None = None
    minutes: int | None = None
    pages: int | None = None
    tasks: int | None = None
    notes: str | None = None


class LearningLogResponse(LearningLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    goal_id: int
    user_id: int
    created_at: dt.datetime
    updated_at: dt.datetime
