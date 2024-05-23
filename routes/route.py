from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.models import DeleteRectangleResponse, Rectangle, UpdateRectangle, LineSegment
from utils.controller import (
    create,
    update,
    get_one,
    get_all,
    delete,
    detect_intersect
)

router = APIRouter(tags=["rectangles"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=Rectangle)
def create_rectangle(rectangle: Rectangle, db: Session = Depends(get_db)):
    return create(db=db, rectangle=rectangle)


@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=Rectangle)
def get_one_rectangle(id, db: Session = Depends(get_db)):
    return get_one(db=db, id=UUID(id))


@router.patch("/update", status_code=status.HTTP_200_OK, response_model=Rectangle)
def update_rectangle(rectangle: UpdateRectangle, db: Session = Depends(get_db)):
    return update(db=db, rectangle=rectangle)


@router.delete(
    "/delete/{id}", status_code=status.HTTP_200_OK, response_model=DeleteRectangleResponse
)
def delete_rectangle(id, db: Session = Depends(get_db)):
    delete_status = delete(db=db, id=UUID(id))
    if delete_status.detail == "Does not Exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rectangle Not Found"
        )
    else:
        return delete_status


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[Rectangle])
def get_all_rectangles(db: Session = Depends(get_db)):
    return get_all(db=db)


@router.post("/intersect", status_code=status.HTTP_200_OK, response_model=List[Rectangle])
def intersect_rectangle(segment: LineSegment, db: Session = Depends(get_db)):
    return detect_intersect(db=db, segment=segment)

