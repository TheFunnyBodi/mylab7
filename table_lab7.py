import psycopg2
from datetime import datetime

try:
    # Підключення до бази даних
    conn = psycopg2.connect(
        dbname="bd_lab7",
        user="user",
        password="1234",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("Connection successful")

     # Видалення таблиць (якщо необхідно)
    cur.execute("DROP TABLE IF EXISTS ProjectExecutions;")
    cur.execute("DROP TABLE IF EXISTS Employees;")
    cur.execute("DROP TABLE IF EXISTS Projects;")
    cur.execute("DROP TABLE IF EXISTS Positions;")
    cur.execute("DROP TABLE IF EXISTS Departments;")

    # Створення таблиць
    # Створення таблиці Departments
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS Departments (
        department_id SERIAL PRIMARY KEY,
        department_name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) CHECK (phone ~ '^\+?[0-9]*$'),
        room_number INT CHECK (room_number BETWEEN 701 AND 710) NOT NULL
    );
    """)

    # Створення таблиці Positions
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS Positions (
        position_id SERIAL PRIMARY KEY,
        position_name VARCHAR(100) NOT NULL,
        salary DECIMAL(10, 2) NOT NULL,
        bonus_percentage DECIMAL(5, 2) CHECK (bonus_percentage >= 0) NOT NULL
    );
    """)

    # Створення таблиці Employees
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS Employees (
        employee_id SERIAL PRIMARY KEY,
        last_name VARCHAR(50) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        middle_name VARCHAR(50),
        address VARCHAR(255),
        phone VARCHAR(15) CHECK (phone ~ '^\+?[0-9]*$'),
        education VARCHAR(50) CHECK (education IN ('спеціальна', 'середня', 'вища')) NOT NULL,
        department_id INT REFERENCES Departments(department_id),
        position_id INT REFERENCES Positions(position_id)
    );
    """)

    # Створення таблиці Projects
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS Projects (
        project_number SERIAL PRIMARY KEY,
        project_name VARCHAR(100) NOT NULL,
        deadline DATE NOT NULL,
        funding DECIMAL(15, 2) NOT NULL
    );
    """)

    # Створення таблиці ProjectExecutions
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS ProjectExecutions (
        execution_id SERIAL PRIMARY KEY,
        project_number INT REFERENCES Projects(project_number),
        department_id INT REFERENCES Departments(department_id),
        start_date DATE NOT NULL
    );
    """)

    # Додавання даних у таблицю Departments
    departments_data = [
        ('Програмування', '+380501234567', 701),
        ('Дизайн', '+380501234568', 702),
        ('Інформаційні технології', '+380501234569', 703),
    ]
    
    # Додавання даних у таблицю Positions
    positions_data = [
        ('Інженер', 3000.00, 17.00),
        ('Редактор', 2000.00, 12.00),
        ('Програміст', 3500.00, 13.00),
    ]

    # Додавання даних у таблицю Employees
    employees_data = [
          ('Шевченко', 'Дмитро', 'Степанович', 'Львів, вул. Сихівська, 9', '+380501234579', 'середня', 2, 1),
        ('Бойко', 'Олег', 'Анатолійович', 'Київ, вул. Петра Могили, 16', '+380501234581', 'середня', 2, 3),
        ('Костенко', 'Анастасія', 'Вікторівна', 'Полтава, вул. Дружби, 19', '+380501234584', 'вища', 3, 2),
        ('Федоренко', 'Ярослав', 'Романович', 'Київ, вул. Костянтинівська, 21', '+380501234585', 'середня', 2, 2),
        ('Ковалев', 'Дарина', 'Ігорівна', 'Дніпро, вул. Грушевського, 23', '+380501234586', 'вища', 1, 3),
        ('Кудряшов', 'Олексій', 'Сергійович', 'Львів, вул. Винниченка, 27', '+380501234587', 'спеціальна', 3, 2),
        ('Тимошенко', 'Олена', 'Петрівна', 'Одеса, вул. Мечникова, 4', '+380501234588', 'вища', 1, 3),
        ('Степаненко', 'Ірина', 'Анатоліївна', 'Харків, вул. Сумська, 30', '+380501234589', 'вища', 2, 1),
        ('Кравченко', 'Марина', 'Олександрівна', 'Київ, вул. Січових Стрільців, 17', '+380501234590', 'вища', 2, 2),
        ('Соломко', 'Андрій', 'Валерійович', 'Львів, вул. Івана Франка, 22', '+380501234592', 'вища', 1, 3),
        ('Даниленко', 'Олена', 'Володимирівна', 'Запоріжжя, вул. Червоноармійська, 15', '+380501234593', 'спеціальна', 3, 1),
        ('Назаренко', 'Ярослав', 'Сергійович', 'Харків, вул. Пушкінська, 31', '+380501234594', 'середня', 3, 3),
        ('Левицька', 'Оксана', 'Ігорівна', 'Полтава, вул. Бажана, 9', '+380501234595', 'вища', 2, 2),
        ('Степанов', 'Софія', 'Андріївна', 'Запоріжжя, вул. Набережна, 14', '+380501234605', 'середня', 3, 1),
        ('Петренко', 'Петро', 'Петрович', 'Львів, вул. Шевченка, 5', '+380501234571', 'спеціальна', 2, 3),
        ('Сидоренко', 'Олег', 'Олегович', 'Одеса, вул. Леніна, 15', '+380501234572', 'середня', 1, 2),
        ('Гриценко', 'Анна', 'Сергіївна', 'Харків, вул. Гагаріна, 12', '+380501234573', 'вища', 2, 1),
    ]

    cur.executemany("INSERT INTO Departments (department_name, phone, room_number) VALUES (%s, %s, %s)", departments_data)
    cur.executemany("INSERT INTO Positions (position_name, salary, bonus_percentage) VALUES (%s, %s, %s)", positions_data)
    cur.executemany("INSERT INTO Employees (last_name, first_name, middle_name, address, phone, education, department_id, position_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", employees_data)

    # Додавання проектів у таблицю Projects
    projects_data = [
        ('Проект 001', '2024.12.31', 10000.00),
        ('Проект 002', '2025.01.15', 15000.00),
        ('Проект 003', '2025.02.20', 12000.00),
        ('Проект 004', '2025.03.30', 20000.00),
        ('Проект 005', '2025.04.10', 11000.00),
        ('Проект 006', '2025.05.05', 13000.00),
        ('Проект 007', '2025.06.12', 16000.00),
        ('Проект 008', '2025.07.15', 18000.00),
        ('Проект 009', '2025.08.20', 19000.00),
        ('Проект 010', '2025.09.30', 21000.00),
        ('Проект 011', '2025.10.05', 22000.00),
        ('Проект 012', '2025.11.15', 25000.00),
    ]

    cur.executemany("INSERT INTO Projects (project_name, deadline, funding) VALUES (%s, %s, %s)", projects_data)

    # Додавання виконання проектів у таблицю ProjectExecutions
    project_executions_data = [
        (1, 1, '2024.10.01'),  # Проект 001, відділ Програмування
        (2, 1, '2024.10.01'),  # Проект 002, відділ Програмування
        (5, 1, '2024.10.01'),  # Проект 003, відділ Програмування
        (6, 1, '2024.10.01'),  # Проект 004, відділ Програмування
        (7, 1, '2024.10.01'),  # Проект 005, відділ Програмування
        (3, 2, '2024.10.01'),  # Проект 006, відділ Дизайн
        (4, 2, '2024.10.01'),  # Проект 007, відділ Дизайн
        (8, 2, '2024.10.01'),  # Проект 008, відділ Дизайн
        (9, 2, '2024.10.01'),  # Проект 009, відділ Дизайн
        (10, 3, '2024.10.01'), # Проект 010, відділ Інформаційні технології
        (11, 3, '2024.10.01'), # Проект 011, відділ Інформаційні технології
        (12, 3, '2024.10.01'), # Проект 012, відділ Інформаційні технології
    ]
    
    cur.executemany("INSERT INTO ProjectExecutions (project_number, department_id, start_date) VALUES (%s, %s, %s)", project_executions_data)

    conn.commit()
    print("База даних та таблиці успішно створені та заповнені даними!")

except Exception as e:
    print("An error occurred:", e)

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("Connection closed")