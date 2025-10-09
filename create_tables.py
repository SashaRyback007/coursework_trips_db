from sqlalchemy import create_engine, text
from models import Base 

engine = create_engine("mysql+pymysql://root:Sasha%2ERyback2007@localhost:3306/trips_db")

Base.metadata.create_all(engine)

print(" Таблиці створені/оновлені успішно")
