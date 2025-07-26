from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime

class User(BaseModel):
    id: str = Field(None, alias="_id")
    username: str
    email: EmailStr
    role: Literal["admin", "staff", "student"]
    is_active: bool
    created_at: datetime
