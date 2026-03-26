import sqlite3
import datetime
DB_NAME = "agro_manager.db"

def get_costs_report():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()

        query = """
        SELECT
            Fields.name,
            Operations.task_name,
            Operations.cost
        FROM Fields
        JOIN Operations ON Operations.field_id = Fields.field_id
        """

        cur.execute(query)
        rows = cur.fetchall()

    print(" FIELD COST REPORT ")
    for row in rows:
        print(f"Field: {row[0]}  Task: {row[1]}  Cost: {row[2]} PLN")


def add_new_field():
    field_name = input("How do you want to name your field: ")
    field_area = float(input("How big is your field: "))

    query = "INSERT INTO Fields (name, area_ha) VALUES (?,?)"

    try:
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute(query, (field_name, field_area))
            con.commit()
        print(f"Field {field_name} added!")
    except Exception as e:
        print(f"Database error: {e}")


def add_operations():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()

        print("\n--- AVAILABLE FIELDS ---")
        cur.execute("SELECT field_id, name FROM Fields")
        rows = cur.fetchall()
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
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute(query, (field_ID, task_name, description, date, cost))
            con.commit()
        print(f"\n Success: '{task_name}' added to database.")
    except Exception as e:
        print(f"\n Database error: {e}")


def delete_operations():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT operation_id, task_name FROM Operations")
        rows = cur.fetchall()

    print("\n--- YOUR OPERATIONS ---")
    if not rows:
        print("No operations to delete.")
        return

    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")
    print("------------------------\n")

    to_delete = int(input("Which operation ID do you want to delete: "))

    try:
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM Operations WHERE operation_id = ?", (to_delete,))
            con.commit()
        print(f"Operation number {to_delete} deleted")
    except Exception as e:
        print(f"\n Database error: {e}")


def delete_field():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT field_id, name FROM Fields")
        rows = cur.fetchall()

    print("\n--- YOUR FIELDS ---")
    if not rows:
        print("No field to delete.")
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
                        with sqlite3.connect(DB_NAME) as con:
                            cur = con.cursor()
                            cur.execute("DELETE FROM Operations WHERE field_id = ?", (to_delete,))
                            cur.execute("DELETE FROM Fields WHERE field_id = ?", (to_delete,))
                            con.commit()
                        print(f"Field {to_delete} deleted.")
                    except Exception as e:
                        print(f"\n Database error: {e}")
                    break
                elif confirmation.capitalize() == "N":
                    print("Deletion cancelled.")
                    break
                else:
                    print("Invalid choice.")


def update_operation_cost():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        
        cur.execute("SELECT operation_id, task_name, cost FROM Operations")
        rows = cur.fetchall()

        if not rows:
            print("No operations to update.")
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
                        cur.execute("UPDATE Operations SET cost = ? WHERE operation_id = ?", (New_cost, ID_change))
                        con.commit()
                        print(f"Cost for operation {ID_change} updated!")
                        return
                    elif confirmation.capitalize() == "N":
                        print("Update cancelled.")
                        return
                    else:
                        print("Invalid choice, type Y or N.")


if __name__ == "__main__":
    delete_field()