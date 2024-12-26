import psycopg2
from psycopg2 import sql

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Помилка підключення: {e}")
        return None

def execute_query(query, params=None):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
            if query.strip().lower().startswith('select'):
                return cursor.fetchall()
            return None
        except Exception as e:
            print(f"Помилка виконання запиту: {e}")
        finally:
            cursor.close()
            connection.close()


def close_connection(connection):
    if connection:
        connection.close()

def test_connection():
    connection = create_connection()
    if connection:
        print("Підключення з базою даних встановлено.")
        connection.close()
    else:
        print("Не вдалося підключитися до бази даних.")

def test_database():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="12345",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM account LIMIT 1;")
        print("Таблиця account знайдена.")
        connection.close()
    except Exception as e:
        print(f"Помилка: {e}")


test_database()