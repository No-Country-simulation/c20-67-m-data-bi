import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *

load_dotenv()

user = os.environ['user']
password = os.environ['password']
port = os.environ['port']
database = os.environ['database']

engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost:{port}/{database}", pool_pre_ping=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

#carga de archivos a poblar
df_cost_of_living = pd.read_csv('Dataset_Cost_of_living_US.csv')
df_canada = pd.read_csv('Dataset_Canada.csv')
df_us = pd.read_csv('Dataset_US.csv')

# Procesar datos de CostOfLiving
for index, row in df_cost_of_living.iterrows():
    location = session.query(Location).filter_by(state_province=row['state']).first()
    if not location:
        location = Location(state_province=row['state'])
        session.add(location)
        session.commit()

    cost_of_living = CostOfLiving(
        location=location,
        case_id=row['case_id'],
        is_metro=row['is_metro'],
        # ... otros atributos
    )
    session.add(cost_of_living)

# Procesar datos de JobPosting (combinando Dataset_Canada y Dataset_US)
for df in [df_canada, df_us]:
    for index, row in df.iterrows():
        location = session.query(Location).filter_by(state_province=row['state']).first()
        if not location:
            location = Location(state_province=row['state'])
            session.add(location)
            session.commit()

        seniority_level = session.query(SeniorityLevel).filter_by(level=row['seniority']).first()
        if not seniority_level:
            seniority_level = SeniorityLevel(level=row['seniority'])
            session.add(seniority_level)
            session.commit()

        industry_type = session.query(IndustryType).filter_by(type=row['industry_type']).first()
        if not industry_type:
            industry_type = IndustryType(type=row['industry_type'])
            session.add(industry_type)
            session.commit()

        job_posting = JobPosting(
            location=location,
            seniority_level=seniority_level,
            industry_type=industry_type,
            # ... otros atributos
        )
        session.add(job_posting)

session.commit()