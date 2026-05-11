from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class City(CityBase):
    id : int
    model_config = ConfigDict(from_attributes=True)


class CityCreate(CityBase):
    pass


class TemperatureBase(BaseModel):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    model_config = ConfigDict(from_attributes=True)
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass
