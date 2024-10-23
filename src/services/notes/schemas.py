from pydantic import BaseModel


class BaseNoteSchema(BaseModel):
    title: str


class CreateNoteSchema(BaseNoteSchema):
    content: str


class NoteResponse(BaseNoteSchema):
    content: str


class CreatedNoteResponse(NoteResponse):
    url: str
