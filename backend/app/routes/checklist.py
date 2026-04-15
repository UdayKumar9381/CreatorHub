from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..core.database import get_db
from ..models.models import User, ChecklistItem
from ..schemas.schemas import ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemOut
from ..dependencies import get_current_user

router = APIRouter(prefix="/checklist", tags=["checklist"])

@router.get("/", response_model=List[ChecklistItemOut])
async def get_checklist_items(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChecklistItem)
        .where(ChecklistItem.user_id == user.id)
        .order_by(ChecklistItem.created_at.desc())
    )
    return result.scalars().all()

@router.post("/", response_model=ChecklistItemOut)
async def create_checklist_item(item_data: ChecklistItemCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_item = ChecklistItem(
        title=item_data.title,
        is_completed=item_data.is_completed,
        priority=item_data.priority,
        category=item_data.category,
        due_date=item_data.due_date,
        user_id=user.id
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.put("/{item_id}", response_model=ChecklistItemOut)
async def update_checklist_item(item_id: int, item_data: ChecklistItemUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChecklistItem).where(ChecklistItem.id == item_id, ChecklistItem.user_id == user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    
    for key, value in item_data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}")
async def delete_checklist_item(item_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChecklistItem).where(ChecklistItem.id == item_id, ChecklistItem.user_id == user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    
    await db.delete(item)
    await db.commit()
    return {"message": "Checklist item deleted successfully"}
