import pandas as pd
import sqlite3

def export_tables(option):
    if option == 1:
        connection = sqlite3.connect("data/user_data.sqlite3")
        data_categories = "SELECT * FROM Categories"
        df = pd.read_sql_query(data_categories, connection)
        df.to_csv("export_categories.csv", index=False)
        print("\n✓ Table of Categories saved as 'export_categories.csv'")
        
        data_transactions = "SELECT * FROM Transactions"
        df = pd.read_sql_query(data_transactions, connection)
        df.to_csv("export_transactions.csv", index=False)
        print("✓ Table of Transactions saved as 'export_transactions.csv'")
        
        connection.close()
    else:
        connection = sqlite3.connect("data/user_data.sqlite3")
        data_categories = "SELECT * FROM Categories"
        df = pd.read_sql_query(data_categories, connection)
        df.to_excel("export_categories.xlsx", index=False)
        print("\n✓ Table of Categories saved as 'export_categories.xlsx'")
        
        data_transactions = "SELECT * FROM Transactions"
        df = pd.read_sql_query(data_transactions, connection)
        df.to_excel("export_transactions.xlsx", index=False)
        print("✓ Table of Transactions saved as 'export_transactions.xlsx'")
        
        connection.close()