from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['user']
password = os.environ['password']
port = os.environ['port']
database = os.environ['database']

engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost:{port}/{database}", pool_pre_ping=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
sesion = Session()


class SeniorityLevel(Base):
    __tablename__ = 'seniority_levels'
    id = Column(Integer, primary_key=True)
    level = Column(String(150), unique=True)
    job_postings = relationship("JobPosting", back_populates="seniority_level")

class IndustryType(Base):
    __tablename__ = 'industry_types'
    id = Column(Integer, primary_key=True)
    type = Column(String(150), unique=True)
    job_postings = relationship("JobPosting", back_populates="industry_type")

class JobPosting(Base):
    __tablename__ = 'job_postings'
    id = Column(Integer, primary_key=True)
    job_title = Column(String(255))
    job_info = Column(String(255))
    position_type_id = Column(Integer, ForeignKey('position_types.id'))
    company = Column(String(255))
    city = Column(String(255))
    location_id = Column(Integer, ForeignKey('locations.id'))
    seniority_level_id = Column(Integer, ForeignKey('seniority_levels.id'))
    work_type = Column(String(255))
    industry_type_id = Column(Integer, ForeignKey('industry_types.id'))
    min_salary = Column(Float)
    max_salary = Column(Float)
    avg_salary = Column(Float)
    company_score = Column(Float)
    sector = Column(String(255))
    skills = Column(Text)
    location = relationship("Location", back_populates="job_postings")
    position_type = relationship("PositionType", back_populates="job_postings")
    seniority_level = relationship("SeniorityLevel", back_populates="job_postings")
    industry_type = relationship("IndustryType", back_populates="job_postings")

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    state = Column(String(255))
    abbreviation = Column(String(150))
    country = Column(String(150))
    job_postings = relationship("JobPosting", back_populates="location")
    cost_of_living = relationship("CostOfLiving", back_populates="location")

class CostOfLiving(Base):
    __tablename__ = 'cost_of_living'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    case_id = Column(Integer)
    is_metro = Column(Boolean)
    area_name = Column(String(255))
    parents = Column(Integer)
    children = Column(Integer)
    housing_cost = Column(Float)
    food_cost = Column(Float)
    transportation_cost = Column(Float)
    healthcare_cost = Column(Float)
    other_necessities_cost = Column(Float)
    childcare_cost = Column(Float)
    taxes = Column(Float)
    total_cost = Column(Float)
    median_family_income = Column(Float)
    
    location = relationship("Location", back_populates="cost_of_living")

class PositionType(Base):
    __tablename__ = 'position_types'
    id = Column(Integer, primary_key=True)
    position = Column(String(255))
    job_postings = relationship("JobPosting", back_populates="position_type")

# Función para crear todas las tablas
def create_all():
    Base.metadata.create_all(engine)

# Llamar a la función para crear las tablas
if __name__ == "__main__":
    create_all()