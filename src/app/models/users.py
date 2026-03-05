from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserSignUp(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError('Password is shorter than 8 characters.')
        if not value.isalnum():
            raise ValueError('Password should be alphanumeric.')
        return value