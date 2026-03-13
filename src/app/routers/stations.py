from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_current_user

router = APIRouter(prefix='/stations', tags=['stations'])

@router.post('/')
async def create_station(station_name: str, current_user=Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"message": f"Station '{station_name}' created successfully by admin {current_user.username}."}
