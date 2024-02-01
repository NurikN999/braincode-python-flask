
from models.BaseModel import BaseModel
import sqlite3

class User (BaseModel):
    def __init__(self, db_path):
        self.table = 'users'
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()


    def create_table(self):
        query = f'''
            CREATE TABLE IF NOT EXISTS {self.table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        '''
        self.cursor.execute(query)
        self.connection.commit()


    def create(self, **kwargs):
        super().create(**kwargs)


    def all(self):
        users = self.cursor.execute(f"SELECT * FROM {self.table}").fetchall()
        return users


    def get_user_by_username(self, username):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def get_user_by_id(self, user_id):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (user_id,))
        return self.cursor.fetchone()
