Структура файлу README.md (Інструкція до проєкту)

1. Опис проєкту
Коротко про систему trips_db та мету порівняння SQL vs ORM.

2. Вимоги до середовища
Python 3.10+

MySQL Server 8.0+

Бібліотеки: sqlalchemy, pymysql, matplotlib, pandas.

3. Налаштування бази даних
Інструкція, як імпортувати ваші .sql файли:

Bash

mysql -u root -p < database/trips_db.sql
4. Встановлення залежностей
Bash

pip install -r requirements.txt

5. Перевірити підключення до бази

python test_connection.py

6. Створити таблиці

python create_tables.py

7. Додати тестові дані

python insert_data.py

8. Перевірити ORM-запити (зі зв’язками)

python queries.py

9. Перевірити SQL-запити (зі зв’язками)

python queries_sql.py

10. Перевірити запити без зв’язків
python queries_no_fk_orm.py

python queries_no_fk_sql.py

11. Особливості реалізації
Короткий опис того, як ви вирішили проблему N+1 у коді або як реалізували перемикання між базами з FK та без FK.