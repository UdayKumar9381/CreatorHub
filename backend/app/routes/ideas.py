from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..core.database import get_db
from ..models.models import User, Idea
from ..schemas.schemas import IdeaCreate, IdeaUpdate, IdeaOut
from ..dependencies import get_current_user
from ..services import idea_service
from ..core.constants import ERROR_MSG_IDEA_NOT_FOUND

router = APIRouter(prefix="/ideas", tags=["ideas"])

@router.get("/", response_model=List[IdeaOut])
async def get_ideas(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await idea_service.get_multi_by_user(db, user_id=user.id)

@router.post("/", response_model=IdeaOut)
async def create_idea(idea_data: IdeaCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await idea_service.create(db, obj_in_data=idea_data.model_dump(), user_id=user.id)

@router.put("/{idea_id}", response_model=IdeaOut)
async def update_idea(idea_id: int, idea_data: IdeaUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    idea = await idea_service.get_by_id_and_user(db, id=idea_id, user_id=user.id)
    if not idea:
        raise HTTPException(status_code=404, detail=ERROR_MSG_IDEA_NOT_FOUND)
    
    return await idea_service.update(db, db_obj=idea, obj_in_data=idea_data.model_dump(exclude_unset=True))

@router.delete("/{idea_id}")
async def delete_idea(idea_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    success = await idea_service.delete_by_id_and_user(db, id=idea_id, user_id=user.id)
    if not success:
        raise HTTPException(status_code=404, detail=ERROR_MSG_IDEA_NOT_FOUND)
    
    return {"message": "Idea deleted successfully"}

