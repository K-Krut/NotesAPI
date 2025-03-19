import logging
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.auth.jwt import get_user_by_jwt_token
from app.crud.notes import create_note_db, get_note_db
from app.schemas.notes import NoteSchema, NoteResponse, NoteParentResponse
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def get_notes():
    pass


@router.get("/{note_id")
def get_note(note_id: int):
    pass


@router.post("/", response_model=NoteResponse)
def create_note(note: NoteSchema, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    try:
        note_record = create_note_db(db, note, user_id)
        note_parent = get_note_db(db, note_record.parent_id)

        return NoteResponse(
            id=note_record.id,
            name=note_record.name,
            details=note_record.details,
            parent=NoteParentResponse.validate(note_parent) if note_parent else None,
            created_at=note_record.created_at,
            updated_at=note_record.updated_at,
        )
    except Exception as error:
        logger.error(f'----#ERROR in POST /api/notes: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")


@router.put("/{note_id")
def get_note(note_id: int):
    pass


@router.patch("/{note_id")
def get_note(note_id: int):
    pass


@router.delete("/{note_id")
def get_note(note_id: int):
    pass


