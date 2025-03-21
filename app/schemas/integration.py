from pydantic import BaseModel


class TextSummarizeSchema(BaseModel):
    text: str
