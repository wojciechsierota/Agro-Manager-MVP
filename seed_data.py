import sqlite3


def seed_database():
    """Seeds the agro_manager database with initial data for testing."""
    conn = sqlite3.connect('agro_manager.db')
    cur = conn.cursor()

    # Adding Fields (Name, Area_ha)
    fields = [
        ('Field A', 6.0),
        ('Field B', 12.2),
        ('Main Field', 25.0)
    ]
    cur.executemany('INSERT INTO Fields (name, area_ha) VALUES (?, ?)', fields)

    # Adding Crops
    crops = [
        ('Strawberry',),
        ('Potatoes',),
        ('Wheat',)
    ]
    cur.exec_many = cur.executemany(
        'INSERT INTO Crops (name) VALUES (?)', crops)

    # Adding Operations (field_id, task_name, description, date, cost)
    operations = [
        (1, 'Planting', 'Variety: Elsanta', '2023-10-15', 1200.50),
        (1, 'Fertilization', 'Saltpetre  200kg/ha', '2024-03-10', 3500.00),
        (2, 'Ploughing', 'Winter deep ploughing', '2023-11-20', 800.00)
    ]
    cur.executemany('''
        INSERT INTO Operations (field_id, task_name, description, date, cost)
        VALUES (?, ?, ?, ?, ?)
    ''', operations)

    conn.commit()
    conn.close()
    print("Database seeded successfully with initial agro data!")


if __name__ == "__main__":
    seed_database()
