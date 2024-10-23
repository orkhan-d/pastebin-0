from fastapi import HTTPException


class InternalServerError(HTTPException):
    def __init__(self, message: str = 'Internal Server Error'):
        super().__init__(
            status_code=500,
            detail=message
        )