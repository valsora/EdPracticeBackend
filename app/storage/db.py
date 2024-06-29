from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = 'postgresql+psycopg2://postgres:psql@localhost/practice_db'

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class VacanciesTable(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    vac_id = Column(String)
    job_name = Column('job_name', String)
    company_name = Column('company_name', String)
    requirement = Column('requirement', String)
    responsibility = Column('responsibility', String)
    schedule = Column('schedule', String)
    experience = Column('experience', String)
    employment = Column('employment', String)
