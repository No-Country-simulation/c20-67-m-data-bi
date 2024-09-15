import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelo_ER import *

load_dotenv()

user = os.environ['user']
password = os.environ['password']
port = os.environ['port']
database = os.environ['database']
ruta_base = os.environ['DATA_DIR']

engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost:{port}/{database}", pool_pre_ping=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)

#carga de archivos a poblar
df_cost_of_living = pd.read_csv(ruta_base +'/cleaned_datasets/cost_of_living.csv')
df_job_postings = pd.read_csv(ruta_base +'/cleaned_datasets/job_postings.csv')
df_industry_type= pd.read_csv(ruta_base +'/cleaned_datasets/industry_type.csv')
df_locations = pd.read_csv(ruta_base +'/cleaned_datasets/locations.csv')
df_position_type = pd.read_csv(ruta_base +'/cleaned_datasets/position_types.csv')
df_seniority= pd.read_csv(ruta_base +'/cleaned_datasets/seniority_levels.csv')

def load_data(df, model_class):
    """
    Carga datos de un DataFrame a una tabla SQLAlchemy.

    Args:
        df: DataFrame con los datos a cargar.
        model_class: Clase SQLAlchemy que representa la tabla.
    """

    session = Session()
    for row in df.itertuples():
        # Obtener los nombres de las columnas de la tabla
        table_columns = [col.name for col in model_class.__table__.columns]
        # Crear un diccionario con los datos del registro
        data_dict = {col: getattr(row, col) for col in table_columns if col in df.columns}
        # Crear una instancia del modelo y agregarla a la sesión
        new_record = model_class(**data_dict)
        session.add(new_record)
    session.commit()
    session.close()

# Load data into each table
load_data(df_cost_of_living, CostOfLiving)
load_data(df_job_postings, JobPosting)
load_data(df_industry_type, IndustryType)
load_data(df_locations, Location)
load_data(df_position_type, PositionType)
load_data(df_seniority, SeniorityLevel)