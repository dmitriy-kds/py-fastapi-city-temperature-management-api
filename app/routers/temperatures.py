import httpx

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app import schemas
from app.models import City
from app.settings import settings

router = APIRouter(
    prefix="/temperatures",
    tags=["temperatures"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_temperatures(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        city_id: int | None = None,
) -> List[type[schemas.Temperature]]:
    return crud.get_all_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )

def fetch_temperature_for_city(client: httpx.Client, city: City) -> float:
    response = client.get(
        url=f"{settings.weather_api_url}/current.json",
        params={"q": city.name, "key": settings.api_key}
    )
    response.raise_for_status()
    return response.json()["current"]["temp_c"]

@router.post("/update")
def update_temperatures_of_all_cities(
        db: Session = Depends(get_db),
) -> dict:
    cities = crud.get_all_cities(db)

    with httpx.Client() as client:
        for city in cities:
            try:
                temperature = fetch_temperature_for_city(client, city)
            except httpx.HTTPStatusError:
                raise HTTPException(
                    status_code=502,
                    detail="External API error"
                )

            crud.create_temperature(
                db=db,
                city_id=city.id,
                temperature=temperature
            )

    return {"detail": f"Updated temperatures for {len(cities)} cities"}
