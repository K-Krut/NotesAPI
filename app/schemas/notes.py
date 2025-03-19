import datetime
from typing import Optional
from pydantic import BaseModel


class NoteSchema(BaseModel):
    name: str
    details: str
    parent_id: Optional[int] = None


class NoteResponse(BaseModel):
    id: int
    name: str
    details: str
    parent: Optional["NoteResponse"] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True