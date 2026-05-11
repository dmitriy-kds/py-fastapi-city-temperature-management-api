from typing import List

from sqlalchemy.orm import Session

from app import schemas, models


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100,
) -> List[type[schemas.City]]:
    return db.query(models.City).offset(skip).limit(limit).all()

def get_city_by_id(
        db: Session,
        city_id: int,
) -> type[schemas.City] | None:
    return db.query(models.City).filter(models.City.id == city_id).first()

def create_city(
        db: Session,
        city: schemas.CityCreate,
) -> schemas.City:
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city

def update_city(
        db: Session,
        city_id: int,
        city: schemas.CityCreate,
) -> type[schemas.City] | None:
    db_city = get_city_by_id(db, city_id)

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    db.commit()
    db.refresh(db_city)

    return db_city

def delete_city(
        db: Session,
        city_id: int,
) -> None:
    db_city = get_city_by_id(db, city_id)
    db.delete(db_city)
    db.commit()

def get_all_temperatures(
        db: Session,
        city_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
) -> List[type[schemas.Temperature]]:
    query = db.query(models.Temperature)

    if city_id:
        query = query.filter(models.Temperature.city_id == city_id)

    return query.offset(skip).limit(limit).all()

def create_temperature(
        db: Session,
        city_id: int,
        temperature: float,
) -> schemas.Temperature:
    db_temperature = models.Temperature(
        city_id=city_id,
        temperature=temperature
    )
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)

    return db_temperature
