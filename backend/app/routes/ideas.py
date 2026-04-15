from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from ..core.database import get_db
from ..core.config import settings
from ..models.models import User, Idea
from ..schemas.schemas import IdeaCreate, IdeaUpdate, IdeaOut, AIResponse

router = APIRouter(prefix="/ideas", tags=["ideas"])
from ..dependencies import get_current_user

@router.get("/", response_model=List[IdeaOut])
async def get_ideas(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Idea).where(Idea.user_id == user.id))
    return result.scalars().all()

@router.post("/", response_model=IdeaOut)
async def create_idea(idea_data: IdeaCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_idea = Idea(
        title=idea_data.title,
        description=idea_data.description,
        status=idea_data.status,
        user_id=user.id
    )
    db.add(new_idea)
    await db.commit()
    await db.refresh(new_idea)
    return new_idea

@router.put("/{idea_id}", response_model=IdeaOut)
async def update_idea(idea_id: int, idea_data: IdeaUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Idea).where(Idea.id == idea_id, Idea.user_id == user.id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    for key, value in idea_data.dict(exclude_unset=True).items():
        setattr(idea, key, value)
    
    await db.commit()
    await db.refresh(idea)
    return idea

@router.delete("/{idea_id}")
async def delete_idea(idea_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Idea).where(Idea.id == idea_id, Idea.user_id == user.id))
    idea = result.scalar_one_or_none()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    
    await db.delete(idea)
    await db.commit()
    return {"message": "Idea deleted successfully"}
