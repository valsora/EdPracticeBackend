from fastapi import FastAPI
from routing.vacancies import router as vacancies


app = FastAPI()
app.include_router(vacancies)