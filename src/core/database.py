import sqlite3

class DataBase():
    def __init__(self):
        try:
            self.connection = sqlite3.connect("data/user_data.sqlite3")
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Categories (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"\
                        "Name VARCHAR(100) NOT NULL,"\
                        "Category INTEGER NOT NULL);")
        except Exception as e:
            print(e)
        self.data = self.check_data()
            
    def check_data(self):
        self.cursor.execute("SELECT * FROM Categories")
        return self.cursor.fetchall()
    
    def insert_values(self, category_name, category_type):
        insert = "INSERT INTO Categories (Name, Category) VALUES (?, ?)"
        values = (category_name, category_type)
        
        self.cursor.execute(insert, values)
        self.connection.commit()