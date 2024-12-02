from pydantic import BaseModel
from typing import TypeVar, Type
from src.db import Base


SchemaType = TypeVar("SchemaType", bound=BaseModel)
DBModelType = TypeVar("DBModelType", bound=Base)  # type: ignore


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
