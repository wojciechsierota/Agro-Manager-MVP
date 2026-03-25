import sqlite3


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


if __name__ == "__main__":
    get_costs_report()
