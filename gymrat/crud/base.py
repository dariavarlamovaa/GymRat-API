from typing import Optional, Type, TypeVar, List

from pydantic import BaseModel
from sqlalchemy.orm import Session

ORMModel = TypeVar("ORMModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# OwnerIDType = int


class ORMRep:
    def __init__(self, model: Type[ORMModel]):
        self._model = model

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ORMModel]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).first()

    def get_many(self, db: Session, *args, skip: int = 0, limit: int = 100, **kwargs) -> List[ORMModel]:
        return db.query(self._model).filter(*args).filter_by(**kwargs).offset(skip).limit(limit).all()