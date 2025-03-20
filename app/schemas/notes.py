import datetime
from typing import Optional, List
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
    name: Optional[str] = None
    details: Optional[str] = None


class NoteFullUpdateSchema(BaseModel):
    name: str
    details: str


class NoteResponseSimple(BaseModel):
    id: int
    name: str
    details: str
    parent_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class NotesListResponse(BaseModel):
    total: int
    offset: int
    notes: List[NoteResponseSimple]
