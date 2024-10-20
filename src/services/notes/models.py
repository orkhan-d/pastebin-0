from src.db.base import BaseWithUUIDPK, Base
from sqlalchemy.orm import Mapped, mapped_column


class Note(BaseWithUUIDPK, Base):
    __tablename__ = 'notes'

    filename: Mapped[str] = mapped_column()
    s3_filename: Mapped[str] = mapped_column()
    uri: Mapped[str] = mapped_column()
