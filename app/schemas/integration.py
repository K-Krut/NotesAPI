from pydantic import BaseModel


class TextSummarizeSchema(BaseModel):
    details: str
