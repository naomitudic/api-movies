from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class DirectorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["James Cameron"])
    biography: Optional[str] = Field(None, max_length=500)

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    biography: Optional[str] = Field(None, max_length=500)

class DirectorResponse(DirectorBase):
    id:int = Field(..., description="Primary key")
    model_config = ConfigDict(from_attributes=True)