import logging
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.auth.jwt import get_user_by_jwt_token
from app.crud.notes import create_note_db
from app.schemas.notes import NoteSchema
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


@router.post("/")
def create_note(note: NoteSchema, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    try:
        return create_note_db(db, note, user_id)
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


