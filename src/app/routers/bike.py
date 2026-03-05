from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data.database import get_db
from src.app.data.models import Bike 
from src.app.models.bikes import BikeCreate, BikeResponse

router = APIRouter(prefix='/bikes', tags=['bikes'])

@router.get('/', response_model=list[BikeResponse])
async def get_bikes(status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Bike)
    if status:
        query = query.where(Bike.status == status)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get('/{bike_id}', response_model=BikeResponse)
async def read_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalars().first()
    
    if not bike:
        raise HTTPException(status_code=404, detail=f'Bike with id {bike_id} not found.')
    return bike

@router.post('/', response_model=BikeResponse, status_code=201)
async def create_bike(bike_data: BikeCreate, db: AsyncSession = Depends(get_db)):
    # Unpack the Pydantic model directly into the SQLAlchemy model
    new_bike = Bike(**bike_data.model_dump())
    
    db.add(new_bike)
    await db.commit()
    await db.refresh(new_bike)
    return new_bike

@router.put('/{bike_id}', response_model=BikeResponse)
async def update_bike(bike_id: int, bike_data: BikeCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalars().first()
    
    if not bike:
        raise HTTPException(status_code=404, detail=f'Bike with id {bike_id} not found.')
        
    # Update attributes manually
    for key, value in bike_data.model_dump().items():
        setattr(bike, key, value)
        
    await db.commit()
    await db.refresh(bike)
    return bike

@router.delete('/{bike_id}')
async def delete_bike(bike_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalars().first()
    
    if not bike:
        raise HTTPException(status_code=404, detail='Bike not found')
        
    await db.delete(bike)
    await db.commit()
    return {"deleted": True}