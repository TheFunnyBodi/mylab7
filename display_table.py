import psycopg2
from tabulate import tabulate

# Підключення до бази даних
def connect_db():
    connection = psycopg2.connect(
        host="localhost",
        database="bd_lab7",
        user="user",
        password="1234"
    )
    return connection

# Функція для отримання даних з таблиці
def fetch_data(table_name):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()
    return column_names, records

# Функція для відображення таблиці
def display_table(table_name, column_names, records):
    print(f"Таблиця: {table_name}")
    print(tabulate(records, headers=column_names, tablefmt='psql'))

if __name__ == "__main__":
    print("Відділ кадрів\n") 
    tables = {
        "departments": "Відділи",
        "employees": "Працівники",
        "positions": "Посади",
        "projects": "Проекти",
        "projectexecutions": "Виконання проектів"
    }
    
    for table_name, display_name in tables.items():
        column_names, records = fetch_data(table_name)
        display_table(display_name, column_names, records)
