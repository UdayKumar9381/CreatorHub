from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

ModelType = TypeVar("ModelType")

class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi_by_user(self, db: AsyncSession, user_id: int) -> List[ModelType]:
        result = await db.execute(select(self.model).where(self.model.user_id == user_id))
        return result.scalars().all()

    async def get_by_id_and_user(self, db: AsyncSession, id: Any, user_id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id, self.model.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, obj_in_data: dict, user_id: Optional[int] = None) -> ModelType:
        if user_id:
            obj_in_data["user_id"] = user_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in_data: dict) -> ModelType:
        for field in obj_in_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_in_data[field])
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: Any) -> bool:
        db_obj = await self.get(db, id)
        if not db_obj:
            return False
        await db.delete(db_obj)
        await db.commit()
        return True

    async def delete_by_id_and_user(self, db: AsyncSession, id: Any, user_id: int) -> bool:
        db_obj = await self.get_by_id_and_user(db, id, user_id)
        if not db_obj:
            return False
        await db.delete(db_obj)
        await db.commit()
        return True
