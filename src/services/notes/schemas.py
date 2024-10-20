from pydantic import BaseModel


class BaseNoteSchema(BaseModel):
    title: str


class CreateNoteSchemaDB(BaseNoteSchema):
    url: str
    s3_filename: str


class CreateNoteSchema(BaseNoteSchema):
    content: str


class NoteResponse(BaseModel):
    url: str
