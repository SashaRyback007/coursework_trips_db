from sqlalchemy import create_engine, text
from datetime import datetime

engine = create_engine("mysql+pymysql://root:Sasha%2ERyback2007@localhost:3306/trips_db_no_fk")

with engine.connect() as conn:
    print("\n Бронювання клієнта Ivan Petrenko:")
    start = datetime.now()
    sql = text("""
        SELECT c.first_name, c.last_name, t.title, t.date, b.seats
        FROM bookings b, clients c, trips t
        WHERE b.client_id = c.client_id AND b.trip_id = t.trip_id
        AND c.first_name = 'Ivan';
    """)
    result = conn.execute(sql)
    print(" Час ORM-запиту 1:", datetime.now() - start)
    for row in result:
        print(f"{row.first_name} {row.last_name} → {row.title}, {row.date}, Seats: {row.seats}")

    print("\n Кількість бронювань на кожну поїздку:")
    start = datetime.now()
    sql2 = text("""
        SELECT t.title, COUNT(b.booking_id) AS total_bookings
        FROM trips t, bookings b
        WHERE t.trip_id = b.trip_id
        GROUP BY t.title;
    """)
    result2 = conn.execute(sql2)
    print(" Час ORM-запиту 2:", datetime.now() - start)
    for row in result2:
        print(f"{row.title}: {row.total_bookings} бронювань")

    print("\n Загальна сума оплат:")
    start = datetime.now()
    sql3 = text("SELECT SUM(amount) AS total_amount FROM payments;")
    result3 = conn.execute(sql3).fetchone()
    print(" Час ORM-запиту 3:", datetime.now() - start)
    print(f"Загальна сума оплат: {result3.total_amount}")
