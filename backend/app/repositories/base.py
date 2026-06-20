from typing import TypeVar, Type, Optional, List, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: UUID) -> Optional[ModelType]:
        return self.db.execute(select(self.model).where(self.model.id == id)).scalar_one_or_none()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = self.db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, id: UUID) -> Optional[ModelType]:
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return obj
        return None
