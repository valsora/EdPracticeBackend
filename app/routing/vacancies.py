from fastapi import APIRouter
from app.schemas.models import ParamsForParsing, Vacancy, VacancyGet
from app.storage.db import database, vacancies_table
import requests

router = APIRouter()


def search_words_to_param_text(name, company, description):
    text = ''
    if name != '':
        text += f'NAME:{name}'
    if company != '':
        if text == '':
            text += f'COMPANY_NAME:{company}'
        else:
            text += f' and COMPANY_NAME:{company}'
    if description != '':
        if text == '':
            text += f'DESCRIPTION:{description}'
        else:
            text += f' and DESCRIPTION:{description}'
    return text


@router.get('/')
async def hello():
    return {'message': 'hello'}


@router.get('/vacancies', response_model=list[VacancyGet])
async def get_all_vacancies():
    query = vacancies_table.select()
    return await database.fetch_all(query=query)


@router.post('/parse')
async def start_parsing(params: ParamsForParsing):
    text = search_words_to_param_text(params.name_text, params.company_text, params.description_text)
    for i in range(19):
        vacancies_get_request_params = {
            'page': i,
            'per_page': 100,
            'text': text,
            'experience': params.experience,
            'employment': params.employment,
            'schedule': params.schedule,
            'area': '113',
        }
        resp = requests.get('https://api.hh.ru/vacancies', params=vacancies_get_request_params)
        if resp.status_code == 200:
            vacs = resp.json()['items']
            for vac in vacs:
                vacation = Vacancy(
                    vac_id=str(vac['id']),
                    job_name=str(vac['name']),
                    company_name=str(vac['employer']['name']),
                    requirement=str(vac['snippet']['requirement']),
                    responsibility=str(vac['snippet']['responsibility']),
                    schedule=str(vac['schedule']['name']),
                    experience=str(vac['experience']['name']),
                    employment=str(vac['employment']['name'])
                )
                print(vacation)
                query = vacancies_table.insert().values(vacation.dict())
                await database.execute(query=query)
    return {'message': 'parsing is done, added to db'}
