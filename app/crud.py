from sqlalchemy.orm import Session

from app import schemas, models


def get_all_cities(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    return db.query(models.City).offset(skip).limit(limit).all()

def get_city_by_id(
        db: Session,
        city_id: int,
):
    return db.query(models.City).filter(models.City.id == city_id).first()

def create_city(
        db: Session,
        city: schemas.CityCreate,
):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city

def update_city(
        db: Session,
        city_id: int,
        city: schemas.CityCreate,
):
    db_city = get_city_by_id(db, city_id)

    db_city.name = city.name
    db_city.additional_info = city.additional_info

    db.commit()
    db.refresh(db_city)

    return db_city

def delete_city(
        db: Session,
        city_id: int,
):
    db_city = get_city_by_id(db, city_id)
    db.delete(db_city)
    db.commit()

#
# def get_all_temperature_records(
#         db: Session,
#         skip: int = 0,
#         limit: int = 100,
# ):
#     return db.query(models.Temperature).offset(skip).limit(limit).all()
#
# def get_temperature_by_city_id(
#         db: Session,
#         city_id: int,
# ):
#     return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()

