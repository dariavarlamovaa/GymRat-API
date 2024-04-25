from typing import Optional, Type, TypeVar, List

from pydantic import BaseModel
from sqlalchemy.orm import Session

ORMModel = TypeVar("ORMModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# OwnerIDType = int


class ORMRep:
    def __init__(self, model: Type[ORMModel]):
        self._model = model

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ORMModel]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).first()

    def get_many(self, db: Session, *args, skip: int = 0, limit: int = 100, **kwargs) -> List[ORMModel]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).offset(skip).limit(limit).all()

    def create(self, db: Session, create_obj: CreateSchemaType):
        obj_data = create_obj.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        model_obj = self._model(**obj_data)
        db.add(model_obj)
        db.commit()
        db.refresh(model_obj)
        return model_obj

    def create_with_owner(self, db: Session, create_obj: CreateSchemaType, owner_id: int):
        obj_data = create_obj.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        model_obj = self._model(**obj_data, owner_id=owner_id)
        db.add(model_obj)
        db.commit()
        db.refresh(model_obj)
        return model_obj

    @staticmethod
    def update(db: Session, db_obj: ORMModel, db_update_schema: UpdateSchemaType) -> ORMModel:
        db_obj_data = db_update_schema.model_dump(exclude_unset=True)
        for field, value in db_obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, db_obj: ORMModel) -> ORMModel:
        db.delete(db_obj)
        db.commit()
        return db_obj
