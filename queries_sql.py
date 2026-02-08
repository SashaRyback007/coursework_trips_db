from sqlalchemy import create_engine, text
from decimal import Decimal
import sys

# Підключення до бази даних
engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db")

def get_bookings_by_client_sql(name='Ivan'):
    """Запит [1]: Деталі виконання поїздки через JOIN 5 таблиць"""
    sql = text("""
        SELECT 
            c.first_name, 
            t.title, 
            dr.last_name AS driver_name, 
            v.registration_number 
        FROM bookings b
        JOIN clients c ON b.client_id = c.client_id
        JOIN trips t ON b.trip_id = t.trip_id
        JOIN triplog tl ON t.trip_id = tl.trip_id
        JOIN drivers dr ON tl.driver_id = dr.driver_id
        JOIN vehicles v ON tl.vehicle_id = v.vehicle_id
        WHERE c.first_name = :name;
    """)
    with engine.connect() as conn:
        result = conn.execute(sql, {"name": name})
        return result.all()

def get_trip_booking_counts_sql():
    """Запит [2]: Кількість бронювань на кожну поїздку (GROUP BY)"""
    sql = text("""
        SELECT t.title, COUNT(b.booking_id) AS total_bookings
        FROM trips t
        LEFT JOIN bookings b ON t.trip_id = b.trip_id
        GROUP BY t.title;
    """)
    with engine.connect() as conn:
        result = conn.execute(sql)
        return result.all()

def get_total_payments_sql():
    """Запит [3]: Загальна сума оплат (SUM)"""
    sql = text("SELECT SUM(amount) AS total_amount FROM payments;")
    with engine.connect() as conn:
        return conn.execute(sql).scalar_one()

# Блок для швидкої перевірки роботи файлу
if __name__ == "__main__":
    print("=== ПЕРЕВІРКА ЧИСТОГО SQL ===")
    try:
        total = get_total_payments_sql()
        print(f"Загальна сума: {total:.2f}" if total else "Сума відсутня")
        
        ivan_trips = get_bookings_by_client_sql('Ivan')
        print(f"Поїздок Івана знайдено: {len(ivan_trips)}")
    except Exception as e:
        print(f"Помилка: {e}")