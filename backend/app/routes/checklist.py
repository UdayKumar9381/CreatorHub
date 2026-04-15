from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..core.database import get_db
from ..models.models import User, ChecklistItem
from ..schemas.schemas import ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemOut
from ..dependencies import get_current_user
from ..services import checklist_service
from ..core.constants import ERROR_MSG_CHECKLIST_NOT_FOUND

router = APIRouter(prefix="/checklist", tags=["checklist"])

@router.get("/", response_model=List[ChecklistItemOut])
async def get_checklist_items(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await checklist_service.get_multi_by_user(db, user_id=user.id)

@router.post("/", response_model=ChecklistItemOut)
async def create_checklist_item(item_data: ChecklistItemCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await checklist_service.create(db, obj_in_data=item_data.model_dump(), user_id=user.id)

@router.put("/{item_id}", response_model=ChecklistItemOut)
async def update_checklist_item(item_id: int, item_data: ChecklistItemUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    item = await checklist_service.get_by_id_and_user(db, id=item_id, user_id=user.id)
    if not item:
        raise HTTPException(status_code=404, detail=ERROR_MSG_CHECKLIST_NOT_FOUND)
    
    return await checklist_service.update(db, db_obj=item, obj_in_data=item_data.model_dump(exclude_unset=True))

@router.delete("/{item_id}")
async def delete_checklist_item(item_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    success = await checklist_service.delete_by_id_and_user(db, id=item_id, user_id=user.id)
    if not success:
        raise HTTPException(status_code=404, detail=ERROR_MSG_CHECKLIST_NOT_FOUND)
    
    return {"message": "Checklist item deleted successfully"}

