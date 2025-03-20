import datetime
from typing import Optional
from pydantic import BaseModel


class NoteSchema(BaseModel):
    name: str
    details: str
    parent_id: Optional[int] = None



class NoteParentResponse(BaseModel):
    id: int
    name: str
    details: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class NoteResponse(BaseModel):
    id: int
    name: str
    details: str
    parent: Optional[NoteParentResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class NoteUpdateSchema(BaseModel):
    name: Optional[str]
    details: Optional[str]


class NoteFullUpdateSchema(BaseModel):
    name: str
    details: str
