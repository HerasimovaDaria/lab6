import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("gerda_database.db")
cur = conn.cursor()

# Створення таблиці "Постачальники"
cur.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_code INTEGER PRIMARY KEY,
        company_name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        bank_account TEXT
    );
""")

# Створення таблиці "Матеріали"
cur.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        material_code INTEGER PRIMARY KEY,
        material_name TEXT NOT NULL,
        price REAL NOT NULL
    );
""")

# Створення таблиці "Поставки"
cur.execute("""
    CREATE TABLE IF NOT EXISTS supplies (
        supply_number INTEGER PRIMARY KEY,
        supply_date DATE,
        supplier_code INTEGER REFERENCES suppliers(supplier_code),
        material_code INTEGER REFERENCES materials(material_code),
        delivery_days INTEGER CHECK (delivery_days >= 1 AND delivery_days <= 7),
        quantity INTEGER,
        CONSTRAINT fk_supplier FOREIGN KEY (supplier_code) REFERENCES suppliers(supplier_code),
        CONSTRAINT fk_material FOREIGN KEY (material_code) REFERENCES materials(material_code)
    );
""")

# Додавання даних у таблицю "Постачальники"
cur.executemany("""
    INSERT INTO suppliers (company_name, contact_person, phone, bank_account)
    VALUES (?, ?, ?, ?);
""", [
    ('Supplier1', 'John Doe', '+123456789', '1234567890123456'),
    ('Supplier2', 'Jane Smith', '+987654321', '6543210987654321'),
    ('Supplier3', 'Bob Johnson', '+111222333', '1111222233334444'),
    ('Supplier4', 'Alice Brown', '+444555666', '4444555566667777')
])

# Додавання даних у таблицю "Матеріали"
cur.executemany("""
    INSERT INTO materials (material_name, price)
    VALUES (?, ?);
""", [
    ('Wood', 50.00),
    ('Lacquer', 20.00),
    ('Steel Parts', 100.00)
])

# Додавання даних у таблицю "Поставки"
cur.executemany("""
    INSERT INTO supplies (supply_date, supplier_code, material_code, delivery_days, quantity)
    VALUES (?, ?, ?, ?, ?);
""", [
    ('2023-11-16', 1, 1, 2, 100),
    ('2023-11-17', 2, 2, 3, 50),
    ('2023-11-18', 3, 3, 1, 200),
    ('2023-11-19', 4, 1, 5, 150)
])

# Виведення заголовків стовпців для таблиці "Постачальники"
cur.execute("PRAGMA table_info(suppliers);")
columns = cur.fetchall()
print("\nСтруктура таблиці suppliers:")
for column in columns:
    print(column[1], end='\t')
print()

# Виведення даних для таблиці "Постачальники"
cur.execute("SELECT * FROM suppliers;")
data = cur.fetchall()
print("\nДані таблиці suppliers:")
for row in data:
    print(row)

# Виведення заголовків стовпців для таблиці "Матеріали"
cur.execute("PRAGMA table_info(materials);")
columns = cur.fetchall()
print("\nСтруктура таблиці materials:")
for column in columns:
    print(column[1], end='\t')
print()

# Виведення даних для таблиці "Матеріали"
cur.execute("SELECT * FROM materials;")
data = cur.fetchall()
print("\nДані таблиці materials:")
for row in data:
    print(row)

# Виведення заголовків стовпців для таблиці "Поставки"
cur.execute("PRAGMA table_info(supplies);")
columns = cur.fetchall()
print("\nСтруктура таблиці supplies:")
for column in columns:
    print(column[1], end='\t')
print()

# Виведення даних для таблиці "Поставки"
cur.execute("SELECT * FROM supplies;")
data = cur.fetchall()
print("\nДані таблиці supplies:")
for row in data:
    print(row)

# Виведення результатів запитів

# Запит 1: Відобразити всі поставки, які здійснюються за 3 або менше днів. Відсортувати назви постачальників за алфавітом
query1 = """
    SELECT s.supply_number, s.supply_date, sp.company_name
    FROM supplies s
    JOIN suppliers sp ON s.supplier_code = sp.supplier_code
    WHERE s.delivery_days <= 3
    ORDER BY sp.company_name;
"""
cur.execute(query1)
result1 = cur.fetchall()
print("\nРезультат запиту 1:")
for row in result1:
    print(row)

# Запит 2: Порахувати суму, яку треба сплатити за кожну поставку (запит з обчислювальним полем)
query2 = """
    SELECT supply_number, SUM(quantity * m.price) AS total_cost
    FROM supplies s
    JOIN materials m ON s.material_code = m.material_code
    GROUP BY supply_number;
"""
cur.execute(query2)
result2 = cur.fetchall()
print("\nРезультат запиту 2:")
for row in result2:
    print(row)

# Запит 3: Відобразити всі поставки обраного матеріалу (запит з параметром)
selected_material_code = 1  # Приклад значення
query3 = f"""
    SELECT *
    FROM supplies
    WHERE material_code = {selected_material_code};
"""
cur.execute(query3)
result3 = cur.fetchall()
print("\nРезультат запиту 3:")
for row in result3:
    print(row)

# Запит 4: Порахувати кількість кожного матеріалу, що поставляється кожним постачальником (перехресний запит)
query4 = """
    SELECT sp.company_name, m.material_name, SUM(s.quantity) AS total_quantity
    FROM supplies s
    JOIN suppliers sp ON s.supplier_code = sp.supplier_code
    JOIN materials m ON s.material_code = m.material_code
    GROUP BY sp.company_name, m.material_name;
"""
cur.execute(query4)
result4 = cur.fetchall()
print("\nРезультат запиту 4:")
for row in result4:
    print(row)

# Запит 5: Порахувати загальну кількість кожного матеріалу (підсумковий запит)
query5 = """
    SELECT m.material_name, SUM(s.quantity) AS total_quantity
    FROM supplies s
    JOIN materials m ON s.material_code = m.material_code
    GROUP BY m.material_name;
"""
cur.execute(query5)
result5 = cur.fetchall()
print("\nРезультат запиту 5:")
for row in result5:
    print(row)

# Запит 6: Порахувати кількість поставок від кожного постачальника (підсумковий запит)
query6 = """
    SELECT sp.company_name, COUNT(*) AS total_shipments
    FROM supplies s
    JOIN suppliers sp ON s.supplier_code = sp.supplier_code
    GROUP BY sp.company_name;
"""
cur.execute(query6)
result6 = cur.fetchall()
print("\nРезультат запиту 6:")
for row in result6:
    print(row)

# Закриття підключення та збереження змін
conn.commit()
conn.close()
