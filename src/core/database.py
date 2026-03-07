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
            
    def check_data(self, option):
        if option != 0:
            try:
                self.cursor.execute(f"SELECT Name, Category FROM Categories WHERE Id = {option}")
                return self.cursor.fetchall()
            except Exception as e:
                print(e)
        else:
            self.cursor.execute("SELECT * FROM Categories")
            return self.cursor.fetchall()
    
    def insert_values(self, new_category):
        insert = "INSERT INTO Categories (Name, Category) VALUES (?, ?)"
        values = (new_category.category_name, new_category.category_type)
        
        self.cursor.execute(insert, values)
        self.connection.commit()
        
    def update_values(self, option, value, cat_id):
        if option == 0:
            new_values = (value, cat_id)
            insert = "UPDATE Categories SET Name = ? WHERE Id = ?"
            self.cursor.execute(insert, new_values)
        else:
            new_values = (value, cat_id)
            insert = "UPDATE Categories SET Category = ? WHERE Id = ?"
            self.cursor.execute(insert, new_values)
        self.connection.commit()