import logging
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query

from app.auth.jwt import get_user_by_jwt_token
from app.core.config import settings
from app.crud.notes import create_note_db, get_note_db, delete_note_db, update_note_db, get_user_notes_db, \
    paginate_query
from app.schemas.notes import NoteSchema, NoteResponse, NoteParentResponse, NoteUpdateSchema, NoteFullUpdateSchema, \
    NotesListResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.notes import generate_note_details_response

router = APIRouter()
logger = logging.getLogger(__name__)


def get_checked_note(db: Session, note_id: int, user_id: int):
    note_record = get_note_db(db, note_id)

    if not note_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note not found")

    if not note_record.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access denied")

    return note_record


def update_note_common(note_id: int, fields, db: Session, user_id: int):
    note_record = get_checked_note(db, note_id, user_id)
    update_note_db(db, note_record, fields.model_dump(exclude_unset=True))

    note_parent = get_note_db(db, note_record.parent_id)

    return generate_note_details_response(note_record, note_parent)


@router.get("/", response_model=NotesListResponse)
def get_notes(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_by_jwt_token),
        offset: int = Query(0, alias="offset", ge=0),
        limit: int = Query(10, alias="limit", le=settings.PAGINATION_SIZE)
):
    try:
        query = get_user_notes_db(db, user_id)
        notes = paginate_query(query, offset, limit)

        return NotesListResponse(
            total=query.count(),
            offset=offset + limit,
            notes=notes
        )
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in POST /api/notes/[id]: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")



@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    try:
        note_record = get_checked_note(db, note_id, user_id)
        note_parent = get_note_db(db, note_record.parent_id)

        return generate_note_details_response(note_record, note_parent)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in POST /api/notes/[id]: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")


@router.post("/")
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
def update_note_fully(
        note_id: int,
        fields: NoteFullUpdateSchema,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_by_jwt_token)
):
    try:
        return update_note_common(note_id, fields, db, user_id)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in PUT /api/notes/[id]: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")


@router.patch("/{note_id}")
def update_note(
        note_id: int,
        fields: NoteUpdateSchema,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_by_jwt_token)
):
    try:
        return update_note_common(note_id, fields, db, user_id)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in PATCH /api/notes/[id]: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")



@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user_by_jwt_token)):
    try:
        note_record = get_checked_note(db, note_id, user_id)
        delete_note_db(db, note_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in DELETE /api/notes/[id]: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")




