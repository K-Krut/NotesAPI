from app.schemas.notes import NoteResponse, NoteParentResponse
from app.models.models import Note


def generate_note_details_response(note: Note, parent: Note) -> NoteResponse:
    return NoteResponse(
        id=note.id,
        name=note.name,
        details=note.details,
        parent=NoteParentResponse.validate(parent) if parent else None,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )
