from pydantic import BaseModel
from typing import Optional


class ParamsForParsing(BaseModel):
    name_text: str = ''
    company_text: str = ''
    description_text: str = ''
    experience: list[str] = []
    employment: list[str] = []
    schedule: list[str] = []


class Vacancy(BaseModel):
    vac_id: Optional[str] = None
    job_name: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    company_name: Optional[str] = None
    requirement: Optional[str] = None
    responsibility: Optional[str] = None
    schedule: Optional[str] = None
    experience: Optional[str] = None
    employment: Optional[str] = None


class VacancyGet(Vacancy):
    id: int
