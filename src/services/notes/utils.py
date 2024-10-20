from sqlalchemy.ext.asyncio import AsyncSession

from src.services.notes.models import Note
from src.services.notes.schemas import CreateNoteSchemaDB


async def create_note_db(data: CreateNoteSchemaDB,
                         session: AsyncSession):
    note = Note(
        title=data.title,
        s3_filename=data.s3_filename,
        url=data.url
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note
