from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.evm import calculate_activity, calculate_project
from app.models import Activity, Project
from app.schemas import (
    ActivityEVMResponse,
    ProjectCreate,
    ProjectEVMResponse,
    ProjectResponse,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, session: AsyncSession = Depends(get_session)):
    project = Project(**payload.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.get("", response_model=list[ProjectResponse])
async def list_projects(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Project).order_by(Project.created_at.desc()))
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID, session: AsyncSession = Depends(get_session)):
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, payload: ProjectUpdate, session: AsyncSession = Depends(get_session)):
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: UUID, session: AsyncSession = Depends(get_session)):
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    await session.delete(project)
    await session.commit()


@router.get("/{project_id}/evm", response_model=ProjectEVMResponse)
async def get_project_evm(project_id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Project)
        .where(Project.id == project_id)
        .options(selectinload(Project.activities))
    )
    project = result.scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    activity_responses: list[ActivityEVMResponse] = []
    activity_values: list[dict] = []

    for activity in project.activities:
        indicators = calculate_activity(
            Decimal(str(activity.bac)),
            Decimal(str(activity.planned_progress)),
            Decimal(str(activity.actual_progress)),
            Decimal(str(activity.actual_cost)),
        )
        response_data = {
            "id": activity.id,
            "project_id": activity.project_id,
            "name": activity.name,
            "bac": activity.bac,
            "planned_progress": activity.planned_progress,
            "actual_progress": activity.actual_progress,
            "actual_cost": activity.actual_cost,
            "created_at": activity.created_at,
            "updated_at": activity.updated_at,
            **indicators,
        }
        activity_responses.append(ActivityEVMResponse.model_validate(response_data))
        activity_values.append({"bac": activity.bac, "actual_cost": activity.actual_cost, **indicators})

    return ProjectEVMResponse.model_validate({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "cut_off_date": project.cut_off_date,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "indicators": calculate_project(activity_values),
        "activities": activity_responses,
    })
