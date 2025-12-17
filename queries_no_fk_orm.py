from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal
import sys


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    

class Trip(Base):
    __tablename__ = 'trips'
    trip_id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    

class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    trip_id = Column(Integer, ForeignKey('trips.trip_id'))
    seats = Column(Integer)
   

class Triplog(Base):
    __tablename__ = 'triplog'
    log_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.trip_id'))
    driver_id = Column(Integer, ForeignKey('drivers.driver_id'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'))

class Driver(Base):
    __tablename__ = 'drivers'
    driver_id = Column(Integer, primary_key=True)
    last_name = Column(String)

class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True)
    model = Column(String)
    
class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(10, 2))



engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db_no_fk") # База даних БЕЗ FK
Session = sessionmaker(bind=engine)
session = Session()

print("\n === ТЕСТУВАННЯ ORM (БЕЗ FK) ===")

try:
    session.connection()
except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")
    sys.exit(1)



print("\n [1] Деталі виконання поїздки клієнта Ivan Petrenko (Явний JOIN):")
start = datetime.now()

results = (
    session.query(Client.first_name, Trip.title, Driver.last_name, Vehicle.model)
    .join(Booking, Client.client_id == Booking.client_id)
    .join(Trip, Booking.trip_id == Trip.trip_id)
    .join(Triplog, Trip.trip_id == Triplog.trip_id)
    .join(Driver, Triplog.driver_id == Driver.driver_id)
    .join(Vehicle, Triplog.vehicle_id == Vehicle.vehicle_id)
    .filter(Client.first_name == "Ivan")
    .all()
)

print(" Час ORM-запиту 1 (Явний JOIN):", datetime.now() - start)

for c_fn, t_title, d_ln, v_model in results:
    print(f"{c_fn} → Trip: {t_title}, Driver: {d_ln}, Vehicle: {v_model}")


print("\n [2] Кількість бронювань на кожну поїздку (Явний JOIN):")
start = datetime.now()
results = (
    session.query(Trip.title, func.count(Booking.booking_id).label("total_bookings"))
    .outerjoin(Booking, Trip.trip_id == Booking.trip_id) # Явне зазначення умови приєднання
    .group_by(Trip.title)
    .all()
)
print(" Час ORM-запиту 2 (Явний JOIN):", datetime.now() - start)
for trip, count in results:
    print(f"{trip}: {count} бронювань")


print("\n [3] Загальна сума оплат (ORM Aggregate):")
start = datetime.now()
total_payments = session.query(func.sum(Payment.amount)).scalar()
print(" Час ORM-запиту 3 (Aggregate):", datetime.now() - start)

formatted_total = f"{total_payments:.2f}" if isinstance(total_payments, Decimal) else total_payments
print(f"Загальна сума оплат: {formatted_total}")

session.close()