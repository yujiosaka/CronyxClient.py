from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class Duration(BaseModel):
    years: Optional[int]
    months: Optional[int]
    weeks: Optional[int]
    days: Optional[int]
    hours: Optional[int]
    minutes: Optional[int]
    seconds: Optional[int]


class PostBody(BaseModel):
    jobInterval: Union[str, int, Duration] = Field(alias="job_interval")
    startBuffer: Optional[Union[int, Duration]] = Field(default=None, alias="start_buffer")
    retryInterval: Optional[Union[int, Duration]] = Field(default=None, alias="retry_interval")
    requiredJobNames: Optional[List[str]] = Field(default=None, alias="required_job_names")
    timezone: Optional[str] = Field(default=None)
    noLock: Optional[bool] = Field(default=None, alias="no_lock")
    jobIntervalStartedAt: Optional[str] = Field(default=None, alias="job_interval_started_at")

    @field_validator("jobIntervalStartedAt")
    @classmethod
    def convert_to_isoformat(cls, v: str) -> str:
        if isinstance(v, datetime):
            return v.isoformat()
        return v


class PostResponse(BaseModel):
    id: Optional[str]
    name: str
    interval: int
    interval_started_at: datetime = Field(alias="intervalStartedAt")
    interval_ended_at: datetime = Field(alias="intervalEndedAt")
    is_active: bool = Field(alias="isActive")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
