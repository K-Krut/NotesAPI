import logging
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.auth.jwt import get_user_by_jwt_token
from app.crud.notes import create_note_db, get_note_db
from app.schemas.notes import NoteSchema, NoteResponse, NoteParentResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.notes import generate_note_details_response

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def get_notes():
    pass


@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    try:
        note_record = get_note_db(db, note_id)

        if not note_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note not found")

        if not note_record.user_id == user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied")

        note_parent = get_note_db(db, note_record.parent_id)

        return generate_note_details_response(note_record, note_parent)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in POST /api/notes/[id]: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")


@router.post("/", response_model=NoteResponse)
def create_note(note: NoteSchema, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    try:
        note_record = create_note_db(db, note, user_id)
        note_parent = get_note_db(db, note_record.parent_id)

        return generate_note_details_response(note_record, note_parent)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in POST /api/notes: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")


@router.put("/{note_id}")
def update_note_fully(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    pass


@router.patch("/{note_id}")
def update_note(note_id: int):
    pass


@router.delete("/{note_id}")
def delete_note(note_id: int):
    pass


