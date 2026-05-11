from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app import schemas

router = APIRouter(
    prefix="/cities",
    tags=["cities"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_cities(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
) -> List[schemas.City]:
    return crud.get_all_cities(db, skip=skip, limit=limit)

@router.get("/{city_id}")
def read_city(
        city_id: int,
        db: Session = Depends(get_db),
) -> schemas.City:
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city

@router.post("/", status_code=201)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
) -> schemas.City:
    return crud.create_city(db=db, city=city)

@router.put("/{city_id}")
def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return crud.update_city(db=db, city=city, city_id=city_id)

@router.delete("/{city_id}")
def delete_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    crud.delete_city(db=db, city_id=city_id)
    return {"detail": "City deleted successfully"}
