from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_current_user

router = APIRouter(prefix='/admin', tags=['admin'])

@router.get('/stats')
async def get_admin_stats(current_user=Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return 'Admin Stats'