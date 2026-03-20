import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data.database import get_db
from src.app.data.models import Bike
from src.app.models.bikes import BikeCreate, BikeResponse
from src.app.logger import logger


def get_logger() -> logging.Logger:
    return logger


router = APIRouter(prefix='/bikes', tags=['bikes'])

@router.get('/', response_model=list[BikeResponse])
async def get_bikes(status: Optional[str] = None, db: AsyncSession = Depends(get_db), log: logging.Logger = Depends(get_logger)):
    log.info(f"GET /bikes - filter status={status}")
    query = select(Bike)
    if status:
        query = query.where(Bike.status == status)

    result = await db.execute(query)
    bikes = result.scalars().all()
    log.info(f"GET /bikes - 200 OK - returned {len(bikes)} bikes")
    return bikes

@router.get('/{bike_id}', response_model=BikeResponse)
async def read_bike(bike_id: int, db: AsyncSession = Depends(get_db), log: logging.Logger = Depends(get_logger)):
    log.info(f"GET /bikes/{bike_id} - requested")
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalars().first()

    if not bike:
        log.warning(f"GET /bikes/{bike_id} - 404 Not Found")
        raise HTTPException(status_code=404, detail=f'Bike with id {bike_id} not found.')
    log.info(f"GET /bikes/{bike_id} - 200 OK")
    return bike

@router.post('/', response_model=BikeResponse, status_code=201)
async def create_bike(bike_data: BikeCreate, db: AsyncSession = Depends(get_db), log: logging.Logger = Depends(get_logger)):
    log.info(f"POST /bikes - input: {bike_data.model_dump()}")
    new_bike = Bike(**bike_data.model_dump())

    db.add(new_bike)
    await db.commit()
    await db.refresh(new_bike)
    log.info(f"POST /bikes - 201 Created - bike id={new_bike.id}")
    return new_bike

@router.put('/{bike_id}', response_model=BikeResponse)
async def update_bike(bike_id: int, bike_data: BikeCreate, db: AsyncSession = Depends(get_db), log: logging.Logger = Depends(get_logger)):
    log.info(f"PUT /bikes/{bike_id} - input: {bike_data.model_dump()}")
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalars().first()

    if not bike:
        log.warning(f"PUT /bikes/{bike_id} - 404 Not Found")
        raise HTTPException(status_code=404, detail=f'Bike with id {bike_id} not found.')

    for key, value in bike_data.model_dump().items():
        setattr(bike, key, value)

    await db.commit()
    await db.refresh(bike)
    log.info(f"PUT /bikes/{bike_id} - 200 OK")
    return bike

@router.delete('/{bike_id}')
async def delete_bike(bike_id: int, db: AsyncSession = Depends(get_db), log: logging.Logger = Depends(get_logger)):
    log.info(f"DELETE /bikes/{bike_id} - requested")
    result = await db.execute(select(Bike).where(Bike.id == bike_id))
    bike = result.scalars().first()

    if not bike:
        log.warning(f"DELETE /bikes/{bike_id} - 404 Not Found")
        raise HTTPException(status_code=404, detail='Bike not found')

    await db.delete(bike)
    await db.commit()
    log.info(f"DELETE /bikes/{bike_id} - 200 OK - deleted")
    return {"deleted": True}