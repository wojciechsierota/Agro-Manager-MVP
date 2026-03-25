import sqlite3


def create_database():
    # Łączymy się z bazą (jeśli nie istnieje, zostanie stworzona)
    conn = sqlite3.connect('agro_manager.db')
    cur = conn.cursor()

    # 1. Tabela Pól (Fields)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Fields (
            field_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            area_ha REAL NOT NULL
        )
    ''')

    # 2. Tabela Upraw (Crops) - słownik
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Crops (
            crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # 3. Tabela Zabiegów (Operations) - Serce systemu
    # Łączy pole z konkretną czynnością i datą
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Operations (
            operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER,
            task_name TEXT NOT NULL, -- np. 'Oprysk', 'Siew'
            description TEXT,        -- np. 'Nawóz NPK 15-15-15'
            date TEXT NOT NULL,
            cost REAL,               -- Koszt zabiegu (paliwo, środki)
            FOREIGN KEY (field_id) REFERENCES Fields (field_id)
        )
    ''')

    # 4. Tabela Sprzedaży (Sales) - Finanse i Analityka
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
    print("Baza danych Agro Manager została utworzona")


if __name__ == "__main__":
    create_database()
