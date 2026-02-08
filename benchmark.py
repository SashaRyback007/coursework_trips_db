import time
import csv 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from queries import (
    get_bookings_by_client_orm, 
    get_trip_booking_counts_orm, 
    get_total_payments_orm
)

from queries_sql import (
    get_bookings_by_client_sql, 
    get_trip_booking_counts_sql, 
    get_total_payments_sql
)



engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db")
Session = sessionmaker(bind=engine)
session = Session()

def run_benchmark(query_func, label, iterations=5):
    times = []
    print(f"\n Тестування: {label}")
    for i in range(iterations):
        session.expire_all()
        start = time.perf_counter()
        query_func()
        end = time.perf_counter()
        duration = end - start
        times.append(duration)
        print(f"  Спроба {i+1}: {duration:.6f} сек")
    return times

def main():
    
    tests = [
        
        (get_bookings_by_client_orm, "ORM: Пошук клієнта (N+1)"),
        (get_bookings_by_client_sql, "SQL: Пошук клієнта (JOIN)"),
        
        
        (get_trip_booking_counts_orm, "ORM: Групування"),
        (get_trip_booking_counts_sql, "SQL: Групування"),
        
        
        (get_total_payments_orm, "ORM: Агрегація (SUM)"),
        (get_total_payments_sql, "SQL: Агрегація (SUM)")
    ]

    all_results = []
    for func, label in tests:
        run_times = run_benchmark(func, label)
        avg_time = sum(run_times) / len(run_times)
        
        # Готуємо дані для збереження
        row = [label] + run_times + [avg_time]
        all_results.append(row)

    
    headers = ["Запит", "Спроба 1", "Спроба 2", "Спроба 3", "Спроба 4", "Спроба 5", "Середній час"]
    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(all_results)

    print("\n Тестування завершено! Результати збережено в 'benchmark_results.csv'")
    
if __name__ == "__main__":
    main()