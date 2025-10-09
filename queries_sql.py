from sqlalchemy import create_engine, text
from datetime import datetime

engine = create_engine("mysql+pymysql://root:Sasha%2ERyback2007@localhost:3306/trips_db")

with engine.connect() as conn:

    print("\n Бронювання клієнта Ivan Petrenko:")
    sql1 = text("""
        SELECT c.first_name, c.last_name, t.title, t.date, b.seats
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN trips t ON b.trip_id = t.trip_id
        WHERE c.first_name = 'Ivan';
    """)
    start = datetime.now()
    result1 = conn.execute(sql1)
    print("Час SQL-запиту 1:", datetime.now() - start)
    for row in result1:
        print(f"{row.first_name} {row.last_name} → {row.title}, {row.date}, Seats: {row.seats}")

    
    print("\n Кількість бронювань на кожну поїздку:")
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

    
    print("\n Загальна сума оплат:")
    sql3 = text("""
        SELECT SUM(amount) AS total_amount FROM payments;
    """)
    start = datetime.now()
    result3 = conn.execute(sql3).fetchone()
    print(" Час SQL-запиту 3:", datetime.now() - start)
    print(f"Загальна сума оплат: {result3.total_amount}")
