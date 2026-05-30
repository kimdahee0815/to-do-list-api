from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class todoCreate(BaseModel):
    title: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_done: bool = Field(default=False)
    priority: Optional[int] = Field(default=None, ge=1, le=3)
    category_id: Optional[int] = None

class todoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None  
    is_done: bool
    priority: Optional[int] = None    
    created_at: datetime
    category_id: Optional[int] = None 

    model_config = ConfigDict(from_attributes=True)

class todoList(BaseModel):
    items: list[todoResponse]

    model_config = ConfigDict(from_attributes=True)

class todoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    is_done: Optional[bool] = Field(default=None)
    priority: Optional[int] = Field(default=None, ge=1, le=3)
    category_id: Optional[int] = None

class categoryCreate(BaseModel):
    name: str = Field(max_length=50)

class categoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class categoryList(BaseModel):
    items: list[categoryResponse]

    model_config = ConfigDict(from_attributes=True)

class categoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None)