from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..core.database import get_db
from ..models.models import Project, User
from ..schemas.schemas import ProjectCreate, ProjectUpdate, ProjectOut
from ..dependencies import get_current_user
from ..services import project_service
from ..core.constants import ERROR_MSG_PROJECT_NOT_FOUND

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=ProjectOut)
async def create_project(project_data: ProjectCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await project_service.create(db, obj_in_data=project_data.model_dump(), user_id=current_user.id)

@router.get("/", response_model=List[ProjectOut])
async def get_projects(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await project_service.get_multi_by_user(db, user_id=current_user.id)

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, project_data: ProjectUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = await project_service.get_by_id_and_user(db, id=project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail=ERROR_MSG_PROJECT_NOT_FOUND)
    
    return await project_service.update(db, db_obj=project, obj_in_data=project_data.model_dump(exclude_unset=True))

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = await project_service.delete_by_id_and_user(db, id=project_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail=ERROR_MSG_PROJECT_NOT_FOUND)
    
    return {"message": "Project deleted"}

