from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.data.database import get_db
from src.app.data.models import User
from src.app.models.user import UserCreate, UserResponse, UserSignUp
from src.app.security.security import get_password_hash


router = APIRouter(prefix='/users', tags=['users'])

@router.get('/', response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get('/{user_id}', response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found.')
    return user

@router.post('/', response_model=UserResponse, status_code=201)
async def create_user(user_data: UserSignUp, db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.put('/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found.')
        
    for key, value in user_data.model_dump().items():
        setattr(user, key, value)
        
    await db.commit()
    await db.refresh(user)
    return user

@router.delete('/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail='User not found.')
        
    await db.delete(user)
    await db.commit()
    return {"deleted": True}