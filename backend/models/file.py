from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class File(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="MongoDB ObjectId as string")
    file_name: str = Field(..., min_length=1, max_length=100)
    path: str = Field(..., min_length=1, max_length=100)
    
    uploaded_by: Optional[str] = Field(None, description="User ID or username")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    embedded: bool = Field(default=False)
