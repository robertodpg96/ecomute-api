from fastapi import APIRouter, Depends, HTTPException, Header

def verify_admin_key(api_key: str = Header(...)):
    if api_key != 'eco-admin-secret':
        raise HTTPException(status_code=403, detail='Invalid key')

router = APIRouter(dependencies=[Depends(verify_admin_key)], prefix='/admin', tags=['admin'])

@router.get('/stats')
def get_admin_stats():
    return 'Admin Stats'