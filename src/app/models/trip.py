from pydantic import BaseModel

class TripInput(BaseModel):
    distance_km: float
    battery_level: float