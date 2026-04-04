import datetime
import csv
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
    db = DatabaseManager(DB_NAME)
    db.connect()
    field_name = input("How do you want to name your field: ")
    field_area = db.get_float("How big is your field: ")
    current_crop = input("What is currently planted on this field (or press Enter): ") or "None"
    query = "INSERT INTO Fields (name, area_ha, current_crop) VALUES (?,?,?)"

    try:
        db.execute_query(query, (field_name, field_area, current_crop))
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

    field_ID = db.get_int("On what field you want to do something (enter ID): ")
    found = False

    for row in rows:
        if row[0] == field_ID:
            found = True
            task_name = input("What will you do: ")
            description = input("Description (or press Enter): ") or "---"
            cost = db.get_float("How much will it cost: ")
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            query = "INSERT INTO Operations (field_id, task_name, description, date, cost) VALUES (?, ?, ?, ?, ?)"

            try:
                db.execute_query(query, (field_ID, task_name, description, date, cost))
                print(f"\n Success: '{task_name}' added to database.")
                break
            except Exception as e:
                print(f"\n Database error: {e}")
                break

    if not found:   
        print("Error: ID not found in operations.")
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

    to_delete = db.get_int("Which operation ID do you want to delete: ")
    found = False
    
    for row in rows:
        if row[0] == to_delete:
            found = True
            try:
                db.execute_query("DELETE FROM Operations WHERE operation_id = ?", (to_delete,))
                print(f"Operation number {to_delete} deleted")
            except Exception as e:
                print(f"\n Database error: {e}")
            break


    if not found:
        print("Error: ID not found in operations.")

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

    to_delete = db.get_int("Which field (ID) do you want to delete: ")
    found = False

    for row in rows:
        if row[0] == to_delete:
            found = True
            while True:
                confirmation = input("Are you sure? This deletes field and all operations [Y/N]: ").upper()
                
                if confirmation == "Y":
                    try:
                        db.execute_query("DELETE FROM Operations WHERE field_id = ?", (to_delete,))
                        db.execute_query("DELETE FROM Fields WHERE field_id = ?", (to_delete,))
                        print(f"Field {to_delete} deleted.")
                    except Exception as e:
                        print(f"\n Database error: {e}")
                    break
                
                elif confirmation == "N":
                    print("Deletion cancelled.")
                    break
                
                else:
                    print("Invalid choice. Please type Y or N.")
            
            break


    if not found:
        print("Error: ID not found in operations.")

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

    ID_change = db.get_int("Which task's cost do you want to change (Enter ID): ")
    

    found = False

    for row in rows:
        if row[0] == ID_change:
            found = True
            while True:
                New_cost = db.get_float("What is the new cost: ")
                confirmation = input(f"Are you sure you want to change cost to {New_cost}? [Y/N]: ")
                if confirmation.capitalize() == "Y":
                    db.execute_query("UPDATE Operations SET cost = ? WHERE operation_id = ?", (New_cost, ID_change))
                    print(f"Cost for operation {ID_change} updated!")
                    break
                
                elif confirmation.capitalize() == "N":
                    print("Update cancelled.")
                    break
                
                else:
                    print("Invalid choice, type Y or N.")
            
            break

    if not found:
        print("Error: ID not found in operations.")
        
    db.disconnect()


def update_current_crop():
    db = DatabaseManager(DB_NAME)
    db.connect()
    rows = db.fetch_all("SELECT field_id, name, current_crop FROM Fields")

    for row in rows:
        print(f"ID: {row[0]} | Field: {row[1]} | Current crop: {row[2]}")

    field_id = db.get_int("Which field do you want to update: ")
    new_crop = input("What is now planted: ")

    db.execute_query("UPDATE Fields SET current_crop = ? WHERE field_id = ?", (new_crop, field_id))
    print(f"Crop updated!")
    db.disconnect()


def add_sale():
    db = DatabaseManager(DB_NAME)
    db.connect()
    rows = db.fetch_all("SELECT field_id, name FROM Fields")

    print("\n--- YOUR FIELDS ---")
    if not rows:
        print("No field to show.")
        db.disconnect()
        return

    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")
    print("------------------------\n")

    found = False
    field_id = db.get_int("On which field (ID) have you made some money: ")

    for row in rows:
        if row[0] == field_id:
            found = True
            sold_thing = input("What did you sell: ")
            how_many = db.get_float("How many tons did you sell: ")
            how_much = db.get_float("How much did you earn: ")
            price_per_ton = round(how_much / how_many, 2)
            date = datetime.datetime.now().strftime("%Y-%m-%d")

            query = "INSERT INTO Sales (field_id, crop_name, quantity_tons, total_revenue, price_per_ton, date) VALUES (?, ?, ?, ?, ?, ?)"

            try:
                db.execute_query(query, (field_id, sold_thing, how_many, how_much, price_per_ton, date))
                print(f"\n Success: '{sold_thing}' added to sales.")
            except Exception as e:
                print(f"\n Database error: {e}")

            break

    if not found:
        print("Error: ID not found in operations.")

    db.disconnect()


def get_financial_report():
    db = DatabaseManager(DB_NAME)
    db.connect()

    query = """
    SELECT 
        Fields.name, 
        IFNULL((SELECT SUM(cost) FROM Operations WHERE Operations.field_id = Fields.field_id), 0),
        IFNULL((SELECT SUM(total_revenue) FROM Sales WHERE Sales.field_id = Fields.field_id), 0)
    FROM Fields
    """
    
    rows = db.fetch_all(query)
    db.disconnect()

    print("\n--- FINANCIAL REPORT ---")
    
    for row in rows:
        name = row[0]
        total_costs = row[1]
        total_revenue = row[2]
        
        balance = total_revenue - total_costs
        
        print(f"Field: {name} | Costs: {total_costs} | Income: {total_revenue} | Balance: {balance} PLN")


def export_financial_report():
    db = DatabaseManager(DB_NAME)
    db.connect()
    file_name = "farm_financial_report.csv"

    query = """
    SELECT 
        Fields.name, 
        IFNULL((SELECT SUM(cost) FROM Operations WHERE Operations.field_id = Fields.field_id), 0),
        IFNULL((SELECT SUM(total_revenue) FROM Sales WHERE Sales.field_id = Fields.field_id), 0)
    FROM Fields
    """

    rows = db.fetch_all(query)
    db.disconnect()

    if not rows:
        print("No data to export. Add some operations or sales first.")
        return
    
    try:
        with open(file_name, mode = "w", newline= "" , encoding= "utf-8-sig" ) as file:
            writer = csv.writer(file, delimiter="\t")
            
            writer.writerow(["Field Name", "Total Costs (PLN)", "Total Revenue (PLN)", "Balance (PLN)"])
            
            for row in rows:
                name = row[0]
                costs = row[1]
                revenue = row[2]
                balance = revenue - costs
                

                writer.writerow([name, costs, revenue, balance])

        print(f"Success! Report saved as: {file_name}")
        print("You can now open this file in Excel.")
        
    except Exception as e:
        print(f"Failed to save file: {e}")


def get_field_summary():
    db = DatabaseManager(DB_NAME)
    db.connect()

    rows = db.fetch_all("""
        SELECT 
            Fields.name,
            Fields.area_ha,
            COUNT(Operations.operation_id) as total_operations,
            IFNULL(SUM(Operations.cost), 0) as total_costs,
            IFNULL((SELECT SUM(total_revenue) FROM Sales WHERE Sales.field_id = Fields.field_id), 0) as total_revenue,
            IFNULL((SELECT GROUP_CONCAT(DISTINCT crop_name) FROM Sales WHERE Sales.field_id = Fields.field_id), 'No crops recorded') as crops
        FROM Fields
        LEFT JOIN Operations ON Operations.field_id = Fields.field_id
        GROUP BY Fields.field_id
    """)

    db.disconnect()

    print("\n--- FIELD SUMMARY ---")
    if not rows:
        print("No fields found.")
        return

    for row in rows:
        name = row[0]
        area = row[1]
        operations = row[2]
        costs = row[3]
        revenue = row[4]
        crops = row[5]
        balance = revenue - costs

        print(f"\n  Field: {name} ({area} ha)")
        print(f"  Crops: {crops}")
        print(f"  Operations: {operations}")
        print(f"  Total Costs: {costs} PLN")
        print(f"  Total Revenue: {revenue} PLN")
        print(f"  Balance: {balance} PLN")

    print("\n---------------------")