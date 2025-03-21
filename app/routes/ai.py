import logging
from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.jwt import get_user_by_jwt_token
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.integration import TextSummarizeSchema


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/text/summarize")
def summarize_text(
        details: TextSummarizeSchema,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_by_jwt_token)
):
    try:
        pass
    except HTTPException as error:
        raise error
    except Exception as error:
        logger.error(f'----#ERROR in POST /text/summarize: {error}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error\n{error}")
