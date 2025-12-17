from sqlalchemy import create_engine, text
from datetime import datetime
from decimal import Decimal
import sys

# Підключення до бази даних З FK (зв'язками)
engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db")

# Перевірка підключення
try:
    engine.connect()
except Exception as e:
    print(f"Помилка підключення до бази даних: {e}")
    sys.exit(1)


with engine.connect() as conn:
    print("\n === ТЕСТУВАННЯ ЧИСТОГО SQL (З FK) ===")

    
    print("\n [1] Деталі виконання поїздки клієнта Ivan Petrenko (5 таблиць):")
    start = datetime.now()
    
    sql1 = text("""
        SELECT 
            c.first_name, 
            t.title, 
            dr.last_name AS driver_name, 
            v.registration_number 
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN trips t ON b.trip_id = t.trip_id
        -- Явні приєднання до логістичних таблиць через Triplog
        JOIN triplog tl ON t.trip_id = tl.trip_id
        JOIN drivers dr ON tl.driver_id = dr.driver_id
        JOIN vehicles v ON tl.vehicle_id = v.vehicle_id
        WHERE c.first_name = 'Ivan';
    """)
    result1 = conn.execute(sql1)
    
    print(" Час SQL-запиту 1:", datetime.now() - start)
    for row in result1:
        print(f"{row.first_name} → Trip: {row.title}, Driver: {row.driver_name}, Vehicle: {row.registration_number}")

   
    
    print("\n [2] Кількість бронювань на кожну поїздку:")
    sql2 = text("""
        SELECT t.title, COUNT(b.booking_id) AS total_bookings
        FROM trips t
        LEFT JOIN bookings b ON t.trip_id = b.trip_id
        GROUP BY t.title;
    """)
    start = datetime.now()
    result2 = conn.execute(sql2)
    print(" Час SQL-запиту 2:", datetime.now() - start)
    for row in result2:
        print(f"{row.title}: {row.total_bookings} бронювань")

    
    print("\n [3] Загальна сума оплат:")
    sql3 = text("SELECT SUM(amount) AS total_amount FROM payments;")
    start = datetime.now()
    total_amount = conn.execute(sql3).scalar_one()
    print(" Час SQL-запиту 3:", datetime.now() - start)
    
    formatted_total = f"{total_amount:.2f}" if isinstance(total_amount, Decimal) else total_amount
    print(f"Загальна сума оплат: {formatted_total}")