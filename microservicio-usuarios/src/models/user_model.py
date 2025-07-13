from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
import time

class UserBase(BaseModel):

    tenantId: str = Field(..., description="Unique identifier for the tenant")
    username: str = Field(..., description="Unique username for the tenant")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")

class UserInDB(UserBase):

    userId: str = Field(..., description="Unique ID of the user (UUID)")
    passwordHash: str = Field(..., description="Hashed password using bcrypt")
    createdAt: int = Field(default_factory=lambda: int(time.time()), description="Timestamp of user creation")
    updatedAt: int = Field(default_factory=lambda: int(time.time()), description="Timestamp of last update")
    roles: List[str] = Field(default_factory=lambda: ["customer"], description="List of user roles")

    password: Optional[str] = None

    @validator('password', pre=True, always=True)
    def ensure_password_is_none_for_db(cls, v):

        return None

    class Config:
        
        orm_mode = True