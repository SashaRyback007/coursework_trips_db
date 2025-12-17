from sqlalchemy import create_engine, text

# підключення до бази MySQL
engine = create_engine("mysql+pymysql://root:Sasha%2ERyback2007@localhost:3306/trips_db")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW();"))
        print("✅ Підключення успішне! Поточний час у БД:", result.fetchone())
except Exception as e:
    print("❌ Помилка підключення:", e)
