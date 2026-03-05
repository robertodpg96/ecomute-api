from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class BikesBase(BaseModel):
    model: str
    battery: float = Field(ge=0, le=100)
    status: Literal['available', 'rented', 'maintenance']


class BikeCreate(BikesBase):
    pass


class BikeResponse(BikesBase):
    id: int
    model_config = ConfigDict(from_attributes=True)