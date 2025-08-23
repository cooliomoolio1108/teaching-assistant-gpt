from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime, timezone

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    oid: str
    name: Optional[str] = None
    email: EmailStr
    role: Literal["admin", "staff", "student"] = "student"
    tenant_id: Optional[str] = None      # Microsoft Entra tenant ID
    is_active: bool = True
    status: Literal["active", "suspended", "deleted"] = "active"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True
        orm_mode = True
