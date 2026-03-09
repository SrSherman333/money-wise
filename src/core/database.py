import sqlite3

class DataBaseCategories():
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
        
    def consult_id(self):
        try:
            self.cursor.execute("SELECT id FROM Categories")
            tuples = self.cursor.fetchall()
            list_id_categories = [row[0] for row in tuples]
            return list_id_categories
        except Exception as e:
            print(e)
    
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
        
    def delete_values(self, cat_id):
        self.cursor.execute(f"DELETE FROM Categories WHERE Id = {cat_id}")
        self.connection.commit()
        
class DataBaseTransactions():
    def __init__(self):
        try:
            self.connection = sqlite3.connect("data/user_data.sqlite3")
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"\
                        "Date VARCHAR(10) NOT NULL,"\
                        "Concept VARCHAR(100) NOT NULL,"\
                        "Amount REAL NOT NULL,"\
                        "Category_ID INTEGER NOT NULL);")
        except Exception as e:
            print(e)
            
    def check_data(self, option):
        if option != 0:
            try:
                self.cursor.execute(f"SELECT Date, Concept, Amount, Category_ID FROM Transactions WHERE Id = {option}")
                return self.cursor.fetchall()
            except Exception as e:
                print(e)
        else:
            self.cursor.execute("SELECT * FROM Transactions")
            return self.cursor.fetchall()
        
    def consult_id(self):
        try:
            self.cursor.execute("SELECT id FROM Transactions")
            tuples = self.cursor.fetchall()
            list_id_transactions = [row[0] for row in tuples]
            return list_id_transactions
        except Exception as e:
            print(e)
        
    def insert_values(self, new_transaction):
        insert = "INSERT INTO Transactions (Date, Concept, Amount, Category_ID) VALUES (?, ?, ?, ?)"
        values = (new_transaction.date, new_transaction.concept, new_transaction.amount, new_transaction.category_id)
        
        self.cursor.execute(insert, values)
        self.connection.commit()
        
    def update_values(self, option, value, tran_id):
        if option == 0:
            new_values = (value, tran_id)
            insert = "UPDATE Transactions SET Date = ? WHERE Id = ?"
            self.cursor.execute(insert, new_values)
        elif option == 1:
            new_values = (value, tran_id)
            insert = "UPDATE Transactions SET Concept = ? WHERE Id = ?"
            self.cursor.execute(insert, new_values)
        elif option == 2:
            new_values = (value, tran_id)
            insert = "UPDATE Transactions SET Amount = ? WHERE Id = ?"
            self.cursor.execute(insert, new_values)
        else:
            new_values = (value, tran_id)
            insert = "UPDATE Transactions SET Category_ID = ? WHERE Id = ?"
            self.cursor.execute(insert, new_values)
        self.connection.commit()
        
db = DataBaseCategories()
print(db.check_data(5))