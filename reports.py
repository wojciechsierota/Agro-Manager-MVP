import sqlite3
import datetime
from database_manager import DatabaseManager
DB_NAME = "agro_manager.db"

def get_costs_report():
    db = DatabaseManager(DB_NAME)
    db.connect()

    query = """
        SELECT
            Fields.name,
            Operations.task_name,
            Operations.cost
        FROM Fields
        JOIN Operations ON Operations.field_id = Fields.field_id
        """
    rows = db.fetch_all(query)
    db.disconnect()

    print(" FIELD COST REPORT ")
    for row in rows:
        print(f"Field: {row[0]}  Task: {row[1]}  Cost: {row[2]} PLN")


def add_new_field():
    field_name = input("How do you want to name your field: ")
    field_area = float(input("How big is your field: "))

    query = "INSERT INTO Fields (name, area_ha) VALUES (?,?)"

    try:
        db = DatabaseManager(DB_NAME)
        db.connect()
        db.execute_query(query, (field_name, field_area))
        print(f"Field {field_name} added!")
    except Exception as e:
        print(f"Database error: {e}")
        
    db.disconnect()

def add_operations():
    db = DatabaseManager(DB_NAME)
    db.connect()

    print("\n--- AVAILABLE FIELDS ---")
    rows = db.fetch_all("SELECT field_id, name FROM Fields")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")
    print("------------------------\n")

    field_ID = int(input("On what field you want to do something (enter ID): "))
    task_name = input("What will you do: ")
    description = input("Description (or press Enter): ") or "---"
    cost = float(input("How much will it cost: "))
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    query = "INSERT INTO Operations (field_id, task_name, description, date, cost) VALUES (?, ?, ?, ?, ?)"

    try:
        db.execute_query(query, (field_ID, task_name, description, date, cost))
        print(f"\n Success: '{task_name}' added to database.")
    except Exception as e:
        print(f"\n Database error: {e}")

    db.disconnect()


def delete_operations():
    db = DatabaseManager(DB_NAME)
    db.connect()
    rows = db.fetch_all("SELECT operation_id, task_name FROM Operations")
    print("\n--- YOUR OPERATIONS ---")
    if not rows:
        print("No operations to delete.")
        db.disconnect()
        return

    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")
    print("------------------------\n")

    to_delete = int(input("Which operation ID do you want to delete: "))

    try:
        db.execute_query("DELETE FROM Operations WHERE operation_id = ?", (to_delete,))
        print(f"Operation number {to_delete} deleted")
    except Exception as e:
        print(f"\n Database error: {e}")

    db.disconnect()


def delete_field():
    db = DatabaseManager(DB_NAME)
    db.connect()
    rows = db.fetch_all("SELECT field_id, name FROM Fields")

    print("\n--- YOUR FIELDS ---")
    if not rows:
        print("No field to delete.")
        db.disconnect()
        return

    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")
    print("------------------------\n")

    to_delete = int(input("Which field ID do you want to delete: "))

    for row in rows:
        if row[0] == to_delete:
            while True:
                confirmation = input("Are you sure? This deletes field and all operations [Y/N]: ")
                if confirmation.capitalize() == "Y":
                    try:
                        db.execute_query("DELETE FROM Operations WHERE field_id = ?", (to_delete,))
                        db.execute_query("DELETE FROM Fields WHERE field_id = ?", (to_delete,))
                        print(f"Field {to_delete} deleted.")
                    except Exception as e:
                        print(f"\n Database error: {e}")
                    break
                elif confirmation.capitalize() == "N":
                    print("Deletion cancelled.")
                    break
                else:
                    print("Invalid choice.")

    db.disconnect()


def update_operation_cost():
    db = DatabaseManager(DB_NAME)
    db.connect()
    rows = db.fetch_all("SELECT operation_id, task_name, cost FROM Operations")

    if not rows:
        print("No operations to update.")
        db.disconnect()
        return
        
    print("\n--- YOUR CURRENT OPERATIONS AND COSTS ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Cost: {row[2]}")
    print("------------------------------------------\n")

    ID_change = int(input("Which task's cost do you want to change (Enter ID): "))
    New_cost = float(input("What is the new cost: "))

    for row in rows:
            if row[0] == ID_change:
                while True:
                    confirmation = input(f"Are you sure you want to change cost to {New_cost}? [Y/N]: ")
                    if confirmation.capitalize() == "Y":
                        db.execute_query("UPDATE Operations SET cost = ? WHERE operation_id = ?", (New_cost, ID_change))
                        print(f"Cost for operation {ID_change} updated!")
                        db.disconnect()
                        return
                    elif confirmation.capitalize() == "N":
                        print("Update cancelled.")
                        db.disconnect()
                        return
                    else:
                        print("Invalid choice, type Y or N.")
    db.disconnect()

