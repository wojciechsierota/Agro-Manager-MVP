import sqlite3

def seed_database():
    conn = sqlite3.connect('agro_manager.db')
    cur = conn.cursor()

    fields = [
        ('North Field', 6.0, 'Wheat'),
        ('South Field', 12.2, 'Strawberry'),
        ('East Field', 25.0, 'None')
    ]
    cur.executemany('INSERT INTO Fields (name, area_ha, current_crop) VALUES (?, ?, ?)', fields)

    crops = [
        ('Strawberry',),
        ('Potatoes',),
        ('Wheat',)
    ]
    cur.executemany('INSERT INTO Crops (name) VALUES (?)', crops)

    operations = [
        (1, 'Planting', 'Variety: Elsanta', '2023-10-15', 1200.50),
        (1, 'Fertilization', 'Saltpetre 200kg/ha', '2024-03-10', 3500.00),
        (2, 'Weeding', 'Getting rid of weeds', '2023-04-20', 800.00)
    ]
    cur.executemany('''
        INSERT INTO Operations (field_id, task_name, description, date, cost)
        VALUES (?, ?, ?, ?, ?)
    ''', operations)

    sales = [
        (1, 'Wheat', 5.5, 180.0, 990.0, '2024-08-15'),
        (2, 'Strawberry', 3.2, 850.0, 2720.0, '2024-06-20'),
    ]
    cur.executemany('''
        INSERT INTO Sales (field_id, crop_name, quantity_tons, price_per_ton, total_revenue, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sales)

    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()