from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..core.database import get_db
from ..models.models import Note, User
from ..schemas.schemas import NoteCreate, NoteUpdate, NoteOut
from ..dependencies import get_current_user
from ..services import note_service
from ..core.constants import ERROR_MSG_NOTE_NOT_FOUND

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteOut)
async def create_note(note_data: NoteCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await note_service.create(db, obj_in_data=note_data.model_dump(), user_id=current_user.id)

@router.get("/", response_model=List[NoteOut])
async def get_notes(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await note_service.get_multi_by_user(db, user_id=current_user.id)

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = await note_service.get_by_id_and_user(db, id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail=ERROR_MSG_NOTE_NOT_FOUND)
    return note

@router.put("/{note_id}", response_model=NoteOut)
async def update_note(note_id: int, note_data: NoteUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    note = await note_service.get_by_id_and_user(db, id=note_id, user_id=current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail=ERROR_MSG_NOTE_NOT_FOUND)
    
    return await note_service.update(db, db_obj=note, obj_in_data=note_data.model_dump(exclude_unset=True))

@router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = await note_service.delete_by_id_and_user(db, id=note_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail=ERROR_MSG_NOTE_NOT_FOUND)
    
    return {"message": "Note deleted"}

