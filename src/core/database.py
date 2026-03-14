"""
Database control.

Creation, editing, deletion, and querying of data performed in this file. 
Including both tables: Categories and Transactions

- sqlite3: For database management
- datetime: To filter data with respect to the user's choice
"""

import sqlite3
from datetime import date, timedelta

class DataBaseCategories():
    """
    Class that creates and allows manipulation of the Categories data table
        
    Returns:
        It depends on the option chosen; this will be detailed in each individual method
        
    Raises:
        Invalid indexes
    """
    
    def __init__(self):
        """
        Connecting to and creating the Categories table in the database
        """
        
        try:
            self.connection = sqlite3.connect("data/user_data.sqlite3")
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Categories (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"\
                        "Name VARCHAR(100) NOT NULL,"\
                        "Category VARCHAR(100) NOT NULL);")
        except Exception as e:
            print(e)
            
    def check_data(self, option):
        """
        It is responsible for querying values from the table, either by its index or the entire table
        
        Args:
            option (int): The number that chooses which action to take; if it is 0, it will be understood 
            that the entire table is to be passed, and if it is any other number, it will be understood 
            that it is an index and the data from that index will be passed
            
        Returns:
            list: Returns a list of tuples; if it is a row with its index, it will be a list with only 
            one tuple inside
            
        Raises:
            Invalid index, although the respective validation is already done before calling this method, 
            so there's no way an incorrect index can pass
        """
        
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
        """
        Query only all the IDs in the table
            
        Returns:
            list: Returns a list with a tuple containing all the indices
        """
        
        try:
            self.cursor.execute("SELECT id FROM Categories")
            tuples = self.cursor.fetchall()
            list_id_categories = [row[0] for row in tuples]
            return list_id_categories
        except Exception as e:
            print(e)
    
    def insert_values(self, new_category):
        """
        It is responsible for inserting values into the table (previously written by the user, 
        validated and sent to models.py to ensure that the correct format is followed)
        
        Args:
            new_category (obj): Object created from user input and the model created in models.py
        """
        
        insert = "INSERT INTO Categories (Name, Category) VALUES (?, ?)"
        values = (new_category.category_name, new_category.category_type)
        
        self.cursor.execute(insert, values)
        self.connection.commit()
        
    def update_values(self, option, value, cat_id):
        """
        Update values depending on the corresponding option, since the program allows leaving a parameter 
        blank to imply that the value does not change
        
        Args:
            option (int): number that decides which value will be updated (0: Change name, 1 or any other 
                            number: Change category)
            value (str): Depending on the option chosen, it will be the new Name or Category
            cat_id (int): ID of the category to modify
        """
        
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
        """
        It is responsible for removing a row or category according to its index
        
        Args:
            cat_id (int): Index of the category to be removed
        """
        
        self.cursor.execute(f"DELETE FROM Categories WHERE Id = {cat_id}")
        self.connection.commit()
        
class DataBaseTransactions():
    """
    Class that creates and allows manipulation of the Transactions data table
        
    Returns:
        It depends on the option chosen; this will be detailed in each individual method
        
    Raises:
        Invalid indexes
    """
    
    def __init__(self):
        """
        Connecting to and creating the Transactions table in the database
        """
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
        """
        It is responsible for querying values from the table, either by its index or the entire table
        
        Args:
            option (int): The number that chooses which action to take; if it is 0, it will be understood 
            that the entire table is to be passed, and if it is any other number, it will be understood 
            that it is an index and the data from that index will be passed
            
        Returns:
            list: Returns a list of tuples; if it is a row with its index, it will be a list with only 
            one tuple inside
            
        Raises:
            Invalid index, although the respective validation is already done before calling this method, 
            so there's no way an incorrect index can pass
        """
        
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
        """
        Query only all the IDs in the table
            
        Returns:
            list: Returns a list with a tuple containing all the indices
        """
        
        try:
            self.cursor.execute("SELECT id FROM Transactions")
            tuples = self.cursor.fetchall()
            list_id_transactions = [row[0] for row in tuples]
            return list_id_transactions
        except Exception as e:
            print(e)
        
    def insert_values(self, new_transaction):
        """
        It is responsible for inserting values into the table (previously written by the user, 
        validated and sent to models.py to ensure that the correct format is followed)
        
        Args:
            new_transaction (obj): Object created from user input and the model created in models.py
        """
        
        insert = "INSERT INTO Transactions (Date, Concept, Amount, Category_ID) VALUES (?, ?, ?, ?)"
        values = (new_transaction.date, new_transaction.concept, new_transaction.amount, new_transaction.category_id)
        
        self.cursor.execute(insert, values)
        self.connection.commit()
        
    def update_values(self, option, value, tran_id):
        """
        Update values depending on the corresponding option, since the program allows leaving a parameter 
        blank to imply that the value does not change
        
        Args:
            option (int): Number that decides which value will be updated (0: Change Date, 1: Change Concept,
            2: Change Amount, 3 or any other number: Change Category_ID
                            number: Change category)
            value (str): Depending on the option chosen, it will be the new Date, Concept, Amount or Category_ID
            tran_id (int): ID of the category to modify
        """
        
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
        
    def delete_values(self, tran_id):
        """
        It is responsible for removing a row or category according to its index
        
        Args:
            tran_id (int): Index of the category to be removed
        """
        self.cursor.execute(f"DELETE FROM Transactions WHERE Id = {tran_id}")
        self.connection.commit()
        
    def filter_transactions(self, option, start_date=None, end_date=None):
        """
        It displays transactions depending on an option, an option that decides the dates on which these 
        transactions will be filtered
        
        Args:
            option (int): Number that decides the date of the transactions to be displayed (1: Today, 
                            2: Last 7 days, 3: This month, 4: Previous month, 5: This year, 6: Custom range)
            start_date (str/isoformat): It is only used in option 6; it is to mark the start date in 
                                        the search
            end_date (str/isoformat): It is only used in option 6; it is to mark the final date in the 
                                        search
                                        
        Returns:
            list: List of tuples with transaction data depending on the chosen option
        """
        
        if option == 1: # Today--------------------------------------------------------------------------
            today = date.today().isoformat()
            insert = "SELECT * FROM Transactions WHERE Date = ?"
            self.cursor.execute(insert, (today,))
            return self.cursor.fetchall()
        elif option == 2: # Last 7 days------------------------------------------------------------------
            today = date.today()
            seven_days_ago = today.replace(day=today.day - 6)
            print(seven_days_ago)
            values = (seven_days_ago, today)
            insert = "SELECT * FROM Transactions WHERE Date BETWEEN ? AND ?"
            self.cursor.execute(insert, values)
            return self.cursor.fetchall()
        elif option == 3: # This month-------------------------------------------------------------------
            today = date.today()
            first_day_month = today.replace(day = 1)
            values = (first_day_month, today)
            insert = "SELECT * FROM Transactions WHERE Date BETWEEN ? AND ?"
            self.cursor.execute(insert, values)
            return self.cursor.fetchall()
        elif option == 4: # Previous Month---------------------------------------------------------------
            today = date.today()
            first_day_month = today.replace(day = 1)
            first_day_previus_month = today.replace(month = today.month - 1, day = 1)
            last_day_previus_month = first_day_month - timedelta(days=1)
            values = (first_day_previus_month, last_day_previus_month)
            insert = "SELECT * FROM Transactions WHERE Date BETWEEN ? AND ?"
            self.cursor.execute(insert, values)
            return self.cursor.fetchall()
        elif option == 5: # This Year--------------------------------------------------------------------
            today = date.today()
            first_day_year = today.replace(month = 1, day = 1)
            values = (first_day_year, today)
            insert = "SELECT * FROM Transactions WHERE Date BETWEEN ? AND ?"
            self.cursor.execute(insert, values)
            return self.cursor.fetchall()
        elif option == 6: # Personalizado----------------------------------------------------------------
            values = (start_date, end_date)
            insert = "SELECT * FROM Transactions WHERE Date BETWEEN ? AND ?"
            self.cursor.execute(insert, values)
            return self.cursor.fetchall()