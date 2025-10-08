from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from models import Client, Trip, Booking, Payment, Base

engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db")
Session = sessionmaker(bind=engine)
session = Session()

# --- Клієнти
client1 = Client(first_name="Ivan", last_name="Petrenko", email="ivan@example.com", phone="123456789")
client2 = Client(first_name="Olena", last_name="Shevchenko", email="olena@example.com", phone="987654321")

# --- Поїздки
trip1 = Trip(title="Kyiv Tour", destination="Kyiv", date=date(2025, 10, 10), price=100.0)
trip2 = Trip(title="Lviv Tour", destination="Lviv", date=date(2025, 11, 5), price=150.0)

# --- Бронювання
booking1 = Booking(client=client1, trip=trip1, booking_date=date(2025, 9, 20), seats=2)
booking2 = Booking(client=client2, trip=trip2, booking_date=date(2025, 9, 22), seats=1)

# --- Оплати
payment1 = Payment(booking=booking1, amount=200.0, payment_date=date(2025, 9, 21), method="card")
payment2 = Payment(booking=booking2, amount=150.0, payment_date=date(2025, 9, 23), method="cash")

# Додаємо у сесію
session.add_all([client1, client2, trip1, trip2, booking1, booking2, payment1, payment2])
session.commit()

print("✅ Тестові дані додано успішно")
