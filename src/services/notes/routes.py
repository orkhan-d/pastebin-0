from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.notes import schemas

from src.db.base import get_db_session
from src.services.notes.utils import create_note_db


import os
import aiofiles
from uuid import uuid4
from src.utils.s3 import S3


router = APIRouter(prefix='/notes', tags=['notes'])


@router.post('/', response_model=schemas.NoteResponse)
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

        return schemas.NoteResponse(url=note.url)
    except Exception as e:
        print(e)
    finally:
        os.remove(filename)
