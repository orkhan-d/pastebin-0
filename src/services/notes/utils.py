from uuid import UUID, uuid4

from sqlalchemy import select
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
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note


async def get_note_by_url(url: str,
                          session: AsyncSession):
    stmt = (select(Note.title, Note.s3_filename).
            where(Note.id == generate_id_from_hash(url)))
    result = await session.execute(stmt)
    return result.one_or_none()


def generate_hash_from_id(note_id: int):
    hash = []
    while note_id > 0:
        note_id, r = divmod(note_id, 62)
        hash.append('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'[r])

    return ''.join(hash[::-1])


def generate_id_from_hash(note_hash: str):
    num = 0
    for i, char in enumerate(note_hash):
        power = len(note_hash) - (i + 1)

        num += '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(char) * 62 ** power

    return UUID(int=num)
