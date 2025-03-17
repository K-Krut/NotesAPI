from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_notes():
    pass


@router.get("/{note_id")
def get_note(note_id: int):
    pass


@router.post("/")
def create_note():
    pass


@router.put("/{note_id")
def get_note(note_id: int):
    pass


@router.patch("/{note_id")
def get_note(note_id: int):
    pass


@router.delete("/{note_id")
def get_note(note_id: int):
    pass


