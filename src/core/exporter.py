"""
It handles exporting table data to CSV and XLSX formats

- pandas: To convert the data to Dataframes and then to the formats mentioned above
- sqlite3: To obtain the respective data
"""

import pandas as pd
import sqlite3

def export_tables(option):
    """
    Export the data using one option, as this chooses which of the two formats it will be exported in
    
    Args:
        option (int): Decide in which format it will be exported (1: CSV, 2: XLSX)
        
    Returns:
        Depending on the option chosen, it will return the files in the respective format
    """
    
    if option == 1: # CSV--------------------------------------------------------------------------------
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
    else: #XLSX -----------------------------------------------------------------------------------------
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