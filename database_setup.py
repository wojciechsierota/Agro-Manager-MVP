import sqlite3


def create_database():
    # Connect to the database
    conn = sqlite3.connect('agro_manager.db')
    cur = conn.cursor()

    # 1. Fields Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Fields (
            field_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            area_ha REAL NOT NULL
        )
    ''')

    # 2. Crops Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Crops (
            crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # 3. Operations Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Operations (
            operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER,
            task_name TEXT NOT NULL, -- e.g. 'Spraying', 'Sowing'
            description TEXT,         -- e.g. 'NPK 15-15-15 Fertilizer'
            date TEXT NOT NULL,
            cost REAL,                -- Operation cost (fuel, materials)
            FOREIGN KEY (field_id) REFERENCES Fields (field_id)
        )
    ''')

    # 4. Sales Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER,
            crop_name TEXT NOT NULL,
            quantity_tons REAL NOT NULL,
            price_per_ton REAL NOT NULL,
            total_revenue REAL,
            date TEXT NOT NULL,
            FOREIGN KEY (field_id) REFERENCES Fields (field_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Agro Manager database has been created")


if __name__ == "__main__":
    create_database()
