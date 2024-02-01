
import sqlite3

class BaseModel:

    def __init__(self, db_path):
        self.table = ''
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create(self, **kwargs):
        values = []
        for key, value in kwargs.items():
            values.append(key)

        self.cursor.execute(f"INSERT INTO {self.table} ({', '.join(values)}) VALUES ({', '.join(['?'] * len(values))})", list(kwargs.values()))

        self.connection.commit()


    def delete(self, id):
        self.cursor.execute(f"DELETE FROM {self.table} WHERE id = ?", (id,))
        self.connection.commit()
