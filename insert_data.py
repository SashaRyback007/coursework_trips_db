from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from models import Client, Trip, Booking, Payment, Driver, Vehicle, Route, Tripdetail, Triplog, Base


engine = create_engine("mysql+pymysql://root:Sasha.Ryback2007@localhost:3306/trips_db")
Session = sessionmaker(bind=engine)
session = Session()


session.query(Triplog).delete()
session.query(Tripdetail).delete()
session.query(Route).delete()
session.query(Payment).delete()
session.query(Booking).delete()
session.query(Trip).delete()
session.query(Client).delete()
session.query(Driver).delete()
session.query(Vehicle).delete()
session.commit()




client1 = Client(first_name="Ivan", last_name="Petrenko", email="ivan@example.com", phone="123456789")
client2 = Client(first_name="Olena", last_name="Shevchenko", email="olena@example.com", phone="987654321")


driver1 = Driver(first_name="Mykola", last_name="Koval", phone="333222111", license_number="KV98765")
driver2 = Driver(first_name="Andriy", last_name="Lysenko", phone="444555666", license_number="LYS1234")


vehicle1 = Vehicle(registration_number="AA1234AA", vehicle_type="Bus", model="Mercedes 404", status="Ready")
vehicle2 = Vehicle(registration_number="BC5678BC", vehicle_type="Minibus", model="Ford Transit", status="Ready")


trip1 = Trip(title="Kyiv Tour", destination="Kyiv", date=date(2025, 10, 10), price=100.0)
trip2 = Trip(title="Lviv Tour", destination="Lviv", date=date(2025, 11, 5), price=150.0)


booking1 = Booking(client=client1, trip=trip1, booking_date=date(2025, 9, 20), seats=2)
booking2 = Booking(client=client2, trip=trip2, booking_date=date(2025, 9, 22), seats=1)


payment1 = Payment(booking=booking1, amount=200.0, payment_date=date(2025, 9, 21), method="card")
payment2 = Payment(booking=booking2, amount=150.0, payment_date=date(2025, 9, 23), method="cash")


route1 = Route(trip=trip1, start_location="Railway Station", end_location="Maidan Nezalezhnosti", departure_time="09:00:00", arrival_time="18:00:00")
route2 = Route(trip=trip2, start_location="Market Square", end_location="High Castle", departure_time="10:00:00", arrival_time="17:00:00")


detail1 = Tripdetail(trip=trip1, distance=250, duration=360, fuel_cost=50.0, total_cost=70.0, revenue=180.0)
detail2 = Tripdetail(trip=trip2, distance=180, duration=300, fuel_cost=40.0, total_cost=55.0, revenue=140.0)


log1 = Triplog(
    trip=trip1,
    driver=driver1,
    vehicle=vehicle1,
    actual_departure=datetime(2025, 10, 10, 9, 5),
    actual_arrival=datetime(2025, 10, 10, 17, 50),
    driver_comment="Successful trip, minor delay due to traffic."
)
log2 = Triplog(
    trip=trip2,
    driver=driver2,
    vehicle=vehicle2,
    actual_departure=datetime(2025, 11, 5, 10, 0),
    actual_arrival=datetime(2025, 11, 5, 16, 45),
    driver_comment="Completed ahead of schedule."
)



session.add_all([
    client1, client2, driver1, driver2, vehicle1, vehicle2, trip1, trip2,
    booking1, booking2, payment1, payment2, route1, route2, detail1, detail2,
    log1, log2
])

session.commit()
print("База даних trips_db успішно наповнена тестовими даними для 9 таблиць.")