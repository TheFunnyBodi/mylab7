import psycopg2
from decimal import Decimal

def execute_query(query, params=None):
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

        # Виконання запиту
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        results = cur.fetchall()
        return [[float(val) if isinstance(val, Decimal) else val for val in row] for row in results]

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Connection closed")

# Функція для відображення працівників із зарплатою більше 2000 грн
def show_employees_with_high_salary():
    query = """
    SELECT last_name, first_name, salary 
    FROM employees e 
    JOIN positions p ON e.position_id = p.position_id 
    WHERE salary > 2000 
    ORDER BY last_name;
    """
    results = execute_query(query)
    print("Всі робітники, які мають оклад більший за 2000 грн:")
    for row in results:
        print(f"{row[0]} {row[1]}, {row[2]:.2f} грн") 


# Функція для відображення середньої зарплати в кожному відділі
def show_average_salary_per_department():
    query = """
    SELECT d.department_name, AVG(p.salary) AS avg_salary 
    FROM employees e
    JOIN positions p ON e.position_id = p.position_id
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.department_name;
    """
    results = execute_query(query)
    print("Середня зарплата в кожному відділі:")
    for row in results:
        print(f"{row[0]}, {row[1]:.2f} грн")  

# Функція для відображення проєктів у конкретному відділі
def show_projects_in_department(department_id):
    query = """
    SELECT department_name FROM departments WHERE department_id = %s;
    """
    department_name_result = execute_query(query, (department_id,))
    department_name = department_name_result[0][0] if department_name_result else "Невідомий відділ"

    query = """
    SELECT project_name, deadline, funding
    FROM projects p 
    JOIN ProjectExecutions pe ON p.project_number = pe.project_number
    WHERE pe.department_id = %s;
    """
    results = execute_query(query, (department_id,))
    
    if results:
        print(f"Всі проекти, які виконуються в відділі {department_name}:")
        for row in results:
            print(f"{row[0]} - Дедлайн: {row[1]}, Фінансування: {row[2]:.2f} грн")  
    else:
        print(f"У відділі {department_name} немає проектів.")


# Функція для відображення кількості працівників у кожному відділі
def show_employee_count_per_department():
    query = """
    SELECT d.department_name, COUNT(e.employee_id) AS employee_count
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.department_name;
    """
    results = execute_query(query)
    print("Кількість працівників у кожному відділі:")
    for row in results:
        print(row)


# Функція для розрахунку премій для кожного співробітника
def calculate_bonus_for_each_employee():
    query = """
    SELECT last_name, first_name, salary, (salary * (bonus_percentage / 100)) AS bonus
    FROM employees e
    JOIN positions p ON e.position_id = p.position_id;
    """
    results = execute_query(query)
    print("Розмір премії для кожного співробітника:")
    for row in results:
        print(f"{row[0]} {row[1]}, {row[2]:.2f} грн, {row[3]:.2f} грн")  # Форматування


# Функція для підрахунку рівнів освіти у кожному відділі
def count_education_levels_per_department():
    query = """
    SELECT d.department_name, 
           SUM(CASE WHEN education = 'спеціальна' THEN 1 ELSE 0 END) AS special_education,
           SUM(CASE WHEN education = 'середня' THEN 1 ELSE 0 END) AS middle_education,
           SUM(CASE WHEN education = 'вища' THEN 1 ELSE 0 END) AS higher_education
    FROM employees e
    JOIN departments d ON e.department_id = d.department_id
    GROUP BY d.department_name;
    """
    results = execute_query(query)
    print("Кількість робітників які мають спеціальну, середню, вищу освіту у кожному відділі:")
    for row in results:
        print(f"{row[0]}, спеціальна - {row[1]}, середня - {row[2]}, вища - {row[3]}")


if __name__ == "__main__":
    show_employees_with_high_salary()
    print("\n")
    show_average_salary_per_department()
    print("\n")
    show_projects_in_department(1)
    print("\n")
    show_employee_count_per_department()
    print("\n")
    calculate_bonus_for_each_employee()
    print("\n")
    count_education_levels_per_department()
