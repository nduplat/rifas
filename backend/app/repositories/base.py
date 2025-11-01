from typing import Generic, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model: T):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: str) -> Optional[T]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[T]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in) -> T:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: T, obj_in) -> T:
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: str) -> None:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()