from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func
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
    driver = relationship("Driver", back_populates="driver_logs") 
    vehicle = relationship("Vehicle", back_populates="vehicle_logs") 

class Driver(Base):
    __tablename__ = 'drivers'
    driver_id = Column(Integer, primary_key=True)
    last_name = Column(String)
    driver_logs = relationship("Triplog", back_populates="driver")

class Vehicle(Base):
    __tablename__ = 'vehicles'
    vehicle_id = Column(Integer, primary_key=True)
    model = Column(String)
    vehicle_logs = relationship("Triplog", back_populates="vehicle")
    
class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(10, 2))


engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db")
Session = sessionmaker(bind=engine)
session = Session()



def get_bookings_by_client_orm(name="Ivan"):
    """Запит [1]: Пошук бронювань конкретного клієнта (N+1 навігація)"""
    client = session.query(Client).filter_by(first_name=name).first()
    data = []
    if client:
        for booking in client.bookings:
            # Навігація через об'єкти (те, що ми тестуємо)
            trip_info = {
                "title": booking.trip.title,
                "driver": booking.trip.triplogs[0].driver.last_name if booking.trip.triplogs else "N/A"
            }
            data.append(trip_info)
    return data

def get_trip_booking_counts_orm():
    """Запит [2]: Кількість бронювань на кожну поїздку (JOIN + GROUP BY)"""
    return (
        session.query(Trip.title, func.count(Booking.booking_id).label("total"))
        .outerjoin(Booking)
        .group_by(Trip.title)
        .all()
    )

def get_total_payments_orm():
    """Запит [3]: Загальна сума всіх платежів (Aggregate SUM)"""
    return session.query(func.sum(Payment.amount)).scalar()


if __name__ == "__main__":
    print("\n=== ДЕМОНСТРАЦІЯ ЗАПИТІВ ORM ===")
    
    
    ivan_data = get_bookings_by_client_orm("Ivan")
    print(f"\n[1] Бронювання Івана: Знайдено {len(ivan_data)} поїздок.")
    
   
    stats = get_trip_booking_counts_orm()
    print(f"[2] Статистика поїздок: Отримано дані для {len(stats)} напрямків.")
    
 
    total = get_total_payments_orm()
    formatted_total = f"{total:.2f}" if isinstance(total, Decimal) else "0.00"
    print(f"[3] Загальний оборот: {formatted_total} грн.")

    session.close()