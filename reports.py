import sqlite3
import datetime


def get_costs_report():
    con = sqlite3.connect("agro_manager.db")
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

    con.close()


def add_new_field():
    con = sqlite3.connect("agro_manager.db")
    cur = con.cursor()

    field_name = input("How do you want to name your field: ")
    field_area = float(input("How big is your field: "))

    query = """
    INSERT INTO Fields (name, area_ha) VALUES (?,?)
    """
    cur.execute(query, (field_name, field_area))

    con.commit()
    con.close()
    print(f"Field {field_name} added!")


def add_operations():
    field_ID = int(input("On what field you want to do something (id): "))
    task_name = input("What will you do: ")
    description = input("Do you want to add a description: ") or "---"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    cost = int(input("how much will it cost you: "))
    print(f"{date} adding {task_name} to field {field_ID} with cost {cost}")

    con = sqlite3.connect("agro_manager.db")
    cur = con.cursor()

    query = """
    INSERT INTO Operations (field_id, task_name, description, date, cost) VALUES(?, ?, ?, ?, ?)
    """
    cur.execute(query, (field_ID, task_name, description, date, cost))

    con.commit()
    con.close()
    print(f"Operation -{task_name}- added ")


if __name__ == "__main__":
    get_costs_report()
