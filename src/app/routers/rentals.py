from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data.database import get_db
from src.app.models.rentals import RentalProcessing, RentalResponse
from src.app.data.models import Bike, Rental, User

router = APIRouter(prefix='/rentals', tags=['rentals'])

@router.post('/', response_model=RentalResponse)
async def create_rental(payload: RentalProcessing, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bike).where(Bike.id == payload.bike_id))
    bike = result.scalars().first()
    if not bike:
        raise HTTPException(status_code=404, detail=f"Bike with id {payload.bike_id} not found.")
    
    if bike.status != "available":
        raise HTTPException(status_code=400, detail=f"Bike is currently {bike.status} and cannot be rented.")
        
    bike.status = "rented"
        
    new_rental = Rental(user_id=payload.user_id, bike_id=payload.bike_id)
    
    db.add(new_rental)
    await db.commit()
    await db.refresh(new_rental)
    
    return new_rental