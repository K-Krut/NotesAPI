from typing import Optional
from pydantic import BaseModel


class NoteSchema(BaseModel):
    name: str
    details: str
    user_id: int
    parent_id: Optional[int]

