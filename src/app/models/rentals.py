from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

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

class RentalResponse(BaseModel):
    id: int
    bike_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
