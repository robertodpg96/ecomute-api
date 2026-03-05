from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class RentalOutcome(BaseModel):
    bike_id: int
    user_id: int
    battery: float = Field(ge=0, le=100)

    @field_validator('battery')
    @classmethod
    def validate_battery(cls, value: int):
        if value < 20:
            raise ValueError('Rental cannot be completed')
        return value

class RentalProcessing(BaseModel):
    bike_id: int
    bike_battery: int
    user_id: int

    @model_validator(mode='after')
    def rental_check(self):
        if self.bike_battery < 20:
            raise ValueError('Bike battery too low for rental.')
        return self

class RentalResponse(BaseModel):
    id: int
    bike_id: Optional[int] = None
    user_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)