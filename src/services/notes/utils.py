from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.notes.models import Note
from src.services.notes.schemas import CreateNoteSchema


async def create_note_db(data: CreateNoteSchema,
                         s3_filename: str,
                         uuid: UUID,
                         session: AsyncSession):
    note = Note(
        title=data.title,
        s3_filename=s3_filename,
        url=str(uuid)
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note
