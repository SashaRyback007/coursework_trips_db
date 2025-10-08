from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Client, Trip, Booking, Payment
from datetime import datetime

# Підключення до бази
engine = create_engine("mysql+pymysql://root:Sasha%2ERyback2007@localhost:3306/trips_db")
Session = sessionmaker(bind=engine)
session = Session()

# 1️⃣ Всі бронювання клієнта
print("\n📌 Бронювання клієнта Ivan Petrenko:")
start = datetime.now()   # початок вимірювання
client = session.query(Client).filter_by(first_name="Ivan").first()
for booking in client.bookings:
    print(f"Trip: {booking.trip.title}, Date: {booking.trip.date}, Seats: {booking.seats}")
print("⏱️ Час ORM-запиту 1:", datetime.now() - start)  # <--- різниця часу

# 2️⃣ Кількість бронювань на поїздку
print("\n📌 Кількість бронювань на кожну поїздку:")
start = datetime.now()
results = (
    session.query(Trip.title, func.count(Booking.booking_id))
    .join(Booking)
    .group_by(Trip.title)
    .all()
)
for trip, count in results:
    print(f"{trip}: {count} бронювань")
print("⏱️ Час ORM-запиту 2:", datetime.now() - start)

# 3️⃣ Загальна сума оплат
print("\n📌 Загальна сума оплат:")
start = datetime.now()
total_payments = session.query(func.sum(Payment.amount)).scalar()
print(f"Загальна сума оплат: {total_payments}")
print("⏱️ Час ORM-запиту 3:", datetime.now() - start)
