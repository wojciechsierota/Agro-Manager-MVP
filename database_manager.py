import sqlite3

class DatabaseManager:
    def __init__(self, database):
        self.database = database
        self.con = None

    def connect(self):
        self.con = sqlite3.connect(self.database)

    def disconnect(self):
        if self.con:
            self.con.close()

    def execute_query(self, query, params=None):
        cur = self.con.cursor()
        cur.execute(query, params or ())
        self.con.commit()

    def fetch_all(self, query, params=None):
        cur = self.con.cursor()
        cur.execute(query, params or ())
        return cur.fetchall()
    
    @staticmethod
    def get_float(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input! Please enter a number (e.g., 12.5).")

    @staticmethod
    def get_int(prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input! Please enter a whole number (e.g., 1, 2, 3).")
    

    
