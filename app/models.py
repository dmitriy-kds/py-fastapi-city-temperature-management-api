from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
    Float
)

from app.database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(String(510), nullable=True)


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    temperature = Column(Float, nullable=False)
