import sqlite3
from prettytable import PrettyTable
# Створення PrettyTable для виводу результатів
def print_pretty_table(title, description, data):
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]
    table.add_rows(data)
    print(f"\n{title}:")
    print(table)

# Підключення до бази даних
conn = sqlite3.connect("gerda_database.db")
cur = conn.cursor()

# Отримання списку всіх таблиць у базі даних
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

# Для кожної таблиці виводимо її структуру та дані
for table in tables:
    table_name = table[0]

    # Отримання структури таблиці
    cur.execute(f"PRAGMA table_info({table_name});")
    columns = cur.fetchall()
    print(f"\nСтруктура таблиці {table_name}:")
    for column in columns:
        print(column[1], column[2])

    # Отримання даних таблиці
    cur.execute(f"SELECT * FROM {table_name};")
    data = cur.fetchall()
    print(f"\nДані таблиці {table_name}:")
    for row in data:
        print(row)

# Запит 1
query1 = """
    SELECT s.supply_number, s.supply_date, sp.company_name
    FROM supplies s
    JOIN suppliers sp ON s.supplier_code = sp.supplier_code
    WHERE s.delivery_days <= 3
    ORDER BY sp.company_name;
"""
cur.execute(query1)
result1 = cur.fetchall()
print_pretty_table("Результат запиту 1", cur.description, result1)

# Запит 2
query2 = """
    SELECT supply_number, SUM(quantity * m.price) AS total_cost
    FROM supplies s
    JOIN materials m ON s.material_code = m.material_code
    GROUP BY supply_number;
"""
cur.execute(query2)
result2 = cur.fetchall()
print_pretty_table("Результат запиту 2", cur.description, result2)

# Запит 3
selected_material_code = 1  # Приклад значення
query3 = f"""
    SELECT *
    FROM supplies
    WHERE material_code = {selected_material_code};
"""
cur.execute(query3)
result3 = cur.fetchall()
print_pretty_table("Результат запиту 3", cur.description, result3)

# Запит 4
query4 = """
    SELECT sp.company_name, m.material_name, SUM(s.quantity) AS total_quantity
    FROM supplies s
    JOIN suppliers sp ON s.supplier_code = sp.supplier_code
    JOIN materials m ON s.material_code = m.material_code
    GROUP BY sp.company_name, m.material_name;
"""
cur.execute(query4)
result4 = cur.fetchall()
print_pretty_table("Результат запиту 4", cur.description, result4)

# Запит 5
query5 = """
    SELECT m.material_name, SUM(s.quantity) AS total_quantity
    FROM supplies s
    JOIN materials m ON s.material_code = m.material_code
    GROUP BY m.material_name;
"""
cur.execute(query5)
result5 = cur.fetchall()
print_pretty_table("Результат запиту 5", cur.description, result5)

# Запит 6
query6 = """
    SELECT sp.company_name, COUNT(*) AS total_shipments
    FROM supplies s
    JOIN suppliers sp ON s.supplier_code = sp.supplier_code
    GROUP BY sp.company_name;
"""
cur.execute(query6)
result6 = cur.fetchall()
print_pretty_table("Результат запиту 6", cur.description, result6)

# Закриття підключення
conn.close()
