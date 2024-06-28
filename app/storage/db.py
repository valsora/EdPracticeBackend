from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String
from databases import Database

DB_URL = 'postgresql+psycopg2://postgres:psql@localhost/hh_vacs_db'
engine = create_engine(DB_URL)
metadata = MetaData()

vacancies_table = Table('vacancies_table', metadata,
                        Column('id', Integer(), primary_key=True),
                        Column('vac_id', String()),
                        Column('job_name', String()),
                        Column('company_name', String()),
                        Column('requirement', String()),
                        Column('responsibility', String()),
                        Column('schedule', String()),
                        Column('experience', String()),
                        Column('employment', String()),
                        )

database = Database(DB_URL)
