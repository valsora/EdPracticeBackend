from fastapi import APIRouter, status, Depends
from app.schemas.models import ParamsForParsing, Vacancy, VacancyGet
from app.storage.db import get_session, VacanciesTable, Base, engine
from sqlalchemy.orm import Session
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


@router.get('/drop')
async def recreate_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {'message': 'recreated database'}


@router.get('/', response_model=list[VacancyGet])
async def get_all_vacancies(session: Session = Depends(get_session)):
    return session.query(VacanciesTable).all()


@router.post('/parse', status_code=status.HTTP_201_CREATED)
async def parse_and_create_vacancies(params: ParamsForParsing, session: Session = Depends(get_session)):
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
                vacancy = Vacancy(
                    vac_id=str(vac['id']),
                    job_name=str(vac['name']),
                    company_name=str(vac['employer']['name']),
                    requirement=str(vac['snippet']['requirement']),
                    responsibility=str(vac['snippet']['responsibility']),
                    schedule=str(vac['schedule']['name']),
                    experience=str(vac['experience']['name']),
                    employment=str(vac['employment']['name'])
                )
                session.add(VacanciesTable(**vacancy.dict()))
    session.commit()
    return {'message': 'parsing is done, added vacancies to db'}
