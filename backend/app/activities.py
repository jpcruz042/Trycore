from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Activity, Project
from app.schemas import ActivityCreate, ActivityResponse, ActivityUpdate

router = APIRouter(prefix="/projects/{project_id}/activities", tags=["Activities"])


async def require_project(project_id: UUID, session: AsyncSession) -> Project:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(project_id: UUID, payload: ActivityCreate, session: AsyncSession = Depends(get_session)):
    await require_project(project_id, session)
    activity = Activity(project_id=project_id, **payload.model_dump())
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity


@router.get("", response_model=list[ActivityResponse])
async def list_activities(project_id: UUID, session: AsyncSession = Depends(get_session)):
    await require_project(project_id, session)
    result = await session.execute(
        select(Activity).where(Activity.project_id == project_id).order_by(Activity.created_at.asc())
    )
    return result.scalars().all()


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(project_id: UUID, activity_id: UUID, session: AsyncSession = Depends(get_session)):
    await require_project(project_id, session)
    activity = await session.get(Activity, activity_id)
    if activity is None or activity.project_id != project_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(project_id: UUID, activity_id: UUID, payload: ActivityUpdate, session: AsyncSession = Depends(get_session)):
    await require_project(project_id, session)
    activity = await session.get(Activity, activity_id)
    if activity is None or activity.project_id != project_id:
        raise HTTPException(status_code=404, detail="Activity not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)
    await session.commit()
    await session.refresh(activity)
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(project_id: UUID, activity_id: UUID, session: AsyncSession = Depends(get_session)):
    await require_project(project_id, session)
    activity = await session.get(Activity, activity_id)
    if activity is None or activity.project_id != project_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    await session.delete(activity)
    await session.commit()
