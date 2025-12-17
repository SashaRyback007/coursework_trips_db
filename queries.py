from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal
import sys


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
   
    bookings = relationship("Booking", back_populates="client")

class Trip(Base):
    __tablename__ = 'trips'
    trip_id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    
    
    bookings = relationship("Booking", back_populates="trip")
   
    triplogs = relationship("Triplog", back_populates="trip")

class Booking(Base):
    __tablename__ = 'bookings'
    booking_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    trip_id = Column(Integer, ForeignKey('trips.trip_id'))
    seats = Column(Integer)
    
    
    client = relationship("Client", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")

class Triplog(Base):
    __tablename__ = 'triplog'
    log_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trips.trip_id'))
    driver_id = Column(Integer, ForeignKey('drivers.driver_id'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.vehicle_id'))
    
    trip = relationship("Trip", back_populates="triplogs")
    driver = relationship("Driver", back_populates="triplogs")
    vehicle = relationship("Vehicle", back_populates="triplogs")

class Driver(Base):
    __tablename__ = 'drivers'
    driver_id = Column(Integer, primary_key=True)
    last_name = Column(String)
    triplogs = relationship("Triplog", back_populates="driver")

class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True)
    model = Column(String)
    triplogs = relationship("Triplog", back_populates="vehicle")
    
class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(10, 2))


engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db") # База даних З FK
Session = sessionmaker(bind=engine)
session = Session()

print("\n === ТЕСТУВАННЯ ORM (З FK) ===")

try:
    session.connection()
except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")
    sys.exit(1)


print("\n [1] Бронювання та деталі виконання клієнта Ivan Petrenko (N+1-подібна навігація):")
start = datetime.now()


client = session.query(Client).filter_by(first_name="Ivan").first()

if client:
    
    for booking in client.bookings:
       
        if booking.trip.triplogs:
            log = booking.trip.triplogs[0]
            print(f"Trip: {booking.trip.title}, Driver: {log.driver.last_name}, Vehicle: {log.vehicle.model}")
        else:
            print(f"Trip: {booking.trip.title}, (Деталі виконання відсутні)")

print(" Час ORM-запиту 1 (N+1):", datetime.now() - start)


print("\n [2] Кількість бронювань на кожну поїздку (ORM JOIN):")
start = datetime.now()
results = (
    session.query(Trip.title, func.count(Booking.booking_id).label("total_bookings"))
    .outerjoin(Booking) # ORM автоматично використовує FK для LEFT JOIN
    .group_by(Trip.title)
    .all()
)
print(" Час ORM-запиту 2 (JOIN):", datetime.now() - start)
for trip, count in results:
    print(f"{trip}: {count} бронювань")


print("\n [3] Загальна сума оплат (ORM Aggregate):")
start = datetime.now()
total_payments = session.query(func.sum(Payment.amount)).scalar()
print(" Час ORM-запиту 3 (Aggregate):", datetime.now() - start)

formatted_total = f"{total_payments:.2f}" if isinstance(total_payments, Decimal) else total_payments
print(f"Загальна сума оплат: {formatted_total}")

session.close()