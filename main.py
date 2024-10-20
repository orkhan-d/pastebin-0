from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services import services

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get('/ping')
async def ping():
    return {'ping': 'pong'}


for service in services:
    app.include_router(service.routes.router,
                       prefix='/api')
