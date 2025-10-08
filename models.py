from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Enum
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

class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    destination = Column(String(100))
    date = Column(Date)
    price = Column(DECIMAL(10, 2))

    bookings = relationship("Booking", back_populates="trip")

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
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    amount = Column(DECIMAL(10, 2))
    payment_date = Column(Date)
    method = Column(Enum("cash", "card", "online"))

    booking = relationship("Booking", back_populates="payment")
