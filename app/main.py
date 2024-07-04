from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routing.vacancies import router as vacancies_router
from app.storage.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vacancies_router, prefix='/vacancies', tags=['Vacancies'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/')
async def hello():
    return {'message': 'hello'}
