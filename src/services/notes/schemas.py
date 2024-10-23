from pydantic import BaseModel


class BaseNoteSchema(BaseModel):
    title: str


class CreateNoteSchema(BaseNoteSchema):
    content: str


class NoteResponse(BaseModel):
    url: str
