from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.notes import schemas

from src.services.notes import errors as note_errors
import src.errors as errors

from src.db.base import get_db_session
from src.services.notes.utils import create_note_db, get_note_by_url, generate_hash_from_id


import os
import aiofiles
from uuid import uuid4
from src.utils.s3 import S3


router = APIRouter(prefix='/notes', tags=['notes'])


@router.post('', response_model=schemas.CreatedNoteResponse, status_code=201)
async def create_note(data: schemas.CreateNoteSchema,
                      db_session: AsyncSession = Depends(get_db_session)):
    uuid = uuid4()
    filename = f'{uuid}.txt'

    try:
        # save file locally
        async with aiofiles.open(filename, mode='w') as f:
            await f.write(data.content)

        # upload file to S3
        await S3().upload_file(filename)

        # add note to database
        note = await create_note_db(data, filename, uuid, db_session)

        return schemas.CreatedNoteResponse(title=data.title,
                                           content=data.content,
                                           url=generate_hash_from_id(note.id.int))
    except Exception as e:
        raise errors.InternalServerError(str(e))
    finally:
        os.remove(filename)


@router.get('/{url}', response_model=schemas.NoteResponse)
async def get_notes(url: str,
                    db_session: AsyncSession = Depends(get_db_session)):
    row = await get_note_by_url(url, db_session)
    if row is None:
        raise note_errors.NoteNotFound()

    filename = None
    try:
        filename = await S3().download_file(row.s3_filename)
        async with aiofiles.open(filename, mode='r') as f:
            content = await f.read()

            return schemas.NoteResponse(
                title=row.title,
                content=content
            )
    except Exception as e:
        raise errors.InternalServerError(str(e))
    finally:
        if filename:
            os.remove(filename)
