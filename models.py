from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    
    
    bookings = relationship("Booking", back_populates="client")


class Driver(Base):
    __tablename__ = "drivers"
    driver_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    license_number = Column(String(50))
    
    
    triplogs = relationship("Triplog", back_populates="driver")

class Vehicle(Base):
    __tablename__ = "vehicles"
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    registration_number = Column(String(50), unique=True)
    vehicle_type = Column(String(50))
    model = Column(String(50))
    status = Column(String(30))
    
    
    triplogs = relationship("Triplog", back_populates="vehicle")

class Trip(Base):
    __tablename__ = "trips"
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    destination = Column(String(100))
    date = Column(Date)
    price = Column(DECIMAL(10, 2))
  
    bookings = relationship("Booking", back_populates="trip")
    routes = relationship("Route", back_populates="trip")
    triplogs = relationship("Triplog", back_populates="trip")
    # Зв'язок 1:1
    details = relationship("Tripdetail", back_populates="trip", uselist=False)

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))
    booking_date = Column(Date)
    seats = Column(Integer)
    
  
    client = relationship("Client", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")
    
    payment = relationship("Payment", back_populates="booking", uselist=False)


class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), unique=True) # Unique, якщо оплата 1:1
    amount = Column(DECIMAL(10, 2))
    payment_date = Column(Date)
    method = Column(Enum("cash", "card", "online"))
    

    booking = relationship("Booking", back_populates="payment")

class Route(Base):
    __tablename__ = "routes"
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))
    start_location = Column(String(100))
    end_location = Column(String(100))
    departure_time = Column(String(20))
    arrival_time = Column(String(20))
    
   
    trip = relationship("Trip", back_populates="routes")

class Triplog(Base):
    __tablename__ = "triplog"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.vehicle_id"))
    actual_departure = Column(Date)
    actual_arrival = Column(Date)
    driver_comment = Column(String(500))

    trip = relationship("Trip", back_populates="triplogs")
    driver = relationship("Driver", back_populates="triplogs")
    vehicle = relationship("Vehicle", back_populates="triplogs")

class Tripdetail(Base):
    __tablename__ = "tripdetails"

    trip_id = Column(Integer, ForeignKey("trips.trip_id"), primary_key=True)
    distance = Column(Integer)
    duration = Column(Integer)
    fuel_cost = Column(DECIMAL(10, 2))
    total_cost = Column(DECIMAL(10, 2))
    revenue = Column(DECIMAL(10, 2))
    

    trip = relationship("Trip", back_populates="details")