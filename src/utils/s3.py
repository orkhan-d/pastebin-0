import aioboto3
import aiofiles

from settings import settings


class S3:
    def __init__(self):
        self.session = aioboto3.Session(settings.S3_ACCESS_KEY,
                                        settings.S3_SECRET_KEY,
                                        region_name=settings.S3_REGION)

    def get_client(self):
        return self.session.client(service_name='s3', endpoint_url=settings.S3_URL)

    async def upload_file(self, filename: str):
        async with self.get_client() as s3:
            async with aiofiles.open(filename, mode='rb') as file:
                await s3.upload_fileobj(file, settings.S3_BUCKET_NAME, filename)
                return filename