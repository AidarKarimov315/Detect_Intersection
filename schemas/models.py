from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GenericReponse(BaseModel):
    status: str


class Rectangle(BaseModel):
    id: Optional[UUID]
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float
    x4: float
    y4: float

    class Config:
        orm_mode = True


class DeleteRectangleResponse(BaseModel):
    detail: str


class UpdateRectangle(BaseModel):
    id: UUID
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float
    x4: float
    y4: float

    class Config:
        orm_mode = True


class LineSegment(BaseModel):
    x1: float 
    y1: float
    x2: float
    y2: float