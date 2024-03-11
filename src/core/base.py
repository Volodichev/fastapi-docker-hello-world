from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, BigInteger, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import CONVENTION

metadata = MetaData(naming_convention=CONVENTION)

T = TypeVar('T')


class BaseDB(DeclarativeBase):
    metadata = metadata


class BaseDBModel(BaseDB):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger, autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    created_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp()
    )

    def to_dict(self) -> dict:
        result: dict = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
        return result

    def to_schema(self, schema: Type[T]) -> T:
        return schema(**self.to_dict())

    @classmethod
    def from_dict(cls, data: dict):
        valid_data: dict = {
            key: value
            for key, value in data.items()
            if key in cls.__dict__
        }
        return cls(**valid_data)

    @classmethod
    def from_schema(cls, data: BaseModel):
        return cls.from_dict(data.model_dump())

    def __repr__(self) -> str:
        return str(self.to_dict())
