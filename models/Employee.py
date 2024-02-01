
from models.BaseModel import BaseModel
import sqlite3


class Employee(BaseModel):
    def __init__(self, db_path):
        self.table = 'employee'
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()


    # def create_table(self):
    #     query = f'''
    #         CREATE TABLE IF NOT EXISTS {self.table} (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             username TEXT NOT NULL
    #         )
    #     '''
    #     self.cursor.execute(query)
    #     self.connection.commit()


    def create(self, **kwargs):
        super().create(**kwargs)


    def all(self):
        employee = self.cursor.execute(f"SELECT * FROM {self.table}").fetchall()
        return employee


    def delete(self, id):
        super().delete(id)


    def get_employees_by_department(self, department):
        query = f'''
            SELECT * FROM {self.table} WHERE department = '{department}'
        '''
        employees = self.cursor.execute(query).fetchall()
        return employees

