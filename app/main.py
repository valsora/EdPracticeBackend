from fastapi import FastAPI
from app.routing.vacancies import router as vacancies
from app.storage.db import metadata, engine, database

metadata.create_all(engine)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(vacancies)
