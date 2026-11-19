from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    cut_off_date: date | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    cut_off_date: date | None = None


class ProjectResponse(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime


class ActivityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    bac: Decimal = Field(ge=0)
    planned_progress: Decimal = Field(ge=0, le=100)
    actual_progress: Decimal = Field(ge=0, le=100)
    actual_cost: Decimal = Field(ge=0)


class ActivityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    bac: Decimal | None = Field(default=None, ge=0)
    planned_progress: Decimal | None = Field(default=None, ge=0, le=100)
    actual_progress: Decimal | None = Field(default=None, ge=0, le=100)
    actual_cost: Decimal | None = Field(default=None, ge=0)


class ActivityResponse(ActivityCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime


class EVMIndicators(BaseModel):
    pv: Decimal
    ev: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    cpi_status: Literal["under_budget", "over_budget", "on_budget", "not_available"]
    spi_status: Literal["ahead", "behind", "on_schedule", "not_available"]


class ActivityEVMResponse(ActivityResponse, EVMIndicators):
    pass


class ProjectEVMResponse(ProjectResponse):
    indicators: EVMIndicators
    activities: list[ActivityEVMResponse]
