from fastapi import FastAPI
from app.routing.vacancies import router as vacancies_router
from app.storage.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vacancies_router, prefix='/vacancies', tags=['Vacancies'])


@app.get('/')
async def hello():
    return {'message': 'hello'}
