from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# establish connection between database and client
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#session local is a database session only
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# every model will extend this base
Base = declarative_base()

def get_db():
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#db setup for postgres driver since we are using sqlalchemy this one has no use. but
# in future if you want to write pure sql code then use it
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapiDb', user = 'postgres',
#         password = 'Aditya123', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("Connected to Database Successfully.")
#         break
#     except Exception as error:
#         print("Connecting to database failed due to: ",error)
#         time.sleep(3)