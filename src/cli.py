"""
Console version of the program.

It handles user interaction, with numerical options to navigate between sections

- DataBaseCategories/DataBaseTransactions: Classes for managing database tables
- Analyzer: Class to perform the respective dashboard calculations
- Category/Transaction: Correct format for the data in the respective tables
- export_tables: Function to export tables (CSV/XLSX)
- date/datetime: Module to implement and validate data
"""

from src.core.database import DataBaseCategories, DataBaseTransactions
from src.core.analyzer import Analyzer
from src.core.models import Category, Transaction
from src.core.exporter import export_tables
from datetime import date, datetime

def validation_range(message, min_value, max_value):
    """
    Validates whether the user input meets the specified requirements (with a range, 
    [minimum value, maximum value])
    
    Args:
        message (str): Message to be displayed in the input (example: "Choose an option")
        min_value (int): Minimum possible value for user input
        max_value (int): Maximum possible value for user input
        
    Returns:
        int: User input after verifying its validity
        
    Raises
        Out of range: If the entrance is outside the established limits [min_value. max_value]
        ValueError: If text or symbols are entered
    """
    
    while True:
        try:
            value = int(input(message))
            if min_value <= value <= max_value:
                return value
            print(f"Choose one option from {min_value} and {max_value}")
        except ValueError:
            print("Enter a valid number")
            
def validation_id(message, list_id):
    """
    Validates whether the user input meets the specified requirements 
    (list of numbers, used in this case for table IDs).
    
    Args:
        message (str): Message to be displayed in the input (example: "Choose an option")
        list_id (list): List with a tuple inside, containing all the ids from the tables 
                        (returned by the database)
        
    Returns:
        int: User input after verifying its validity
        
    Raises
        Invalid index: If you enter a number that does not belong to any ID
        ValueError: If text or symbols are entered
    """
    
    while True:
        try:
            value = int(input(message))
            if value in list_id:
                return value
            print("Enter a valid index")
        except ValueError:
            print("Enter only numbers")
            
def validation_edit_values(message, list_id):
    """
    It's the same as the previous function, except this one is used to edit values, 
    since it allows you to press enter without any input and thus keep the same value, 
    something that didn't happen in the previous function.
    
    Args:
        message (str): Message to be displayed in the input (example: "Choose an option")
        list_id (list): List with a tuple inside, containing all the ids from the tables 
                        (returned by the database)
        
    Returns:
        int: User input after verifying its validity
        None: If you do not enter anything (do not edit the value)
        
    Raises
        Invalid index: If you enter a number that does not belong to any ID
    """
    
    while True:
        value = input(message)
        if value.isdigit() and int(value) in list_id:
            return int(value)
        elif value == "":
            print("The type was not updated")
            return None
        else:
            print("Enter a valid index")
            
def validation_date(message):
    """
    Validates whether what the user entered is actually a valid date
    
    Args:
        message (str): Message to be displayed in the input (example: "Choose an option")
        
    Returns:
        str/isoformat: The date entered, if it was written correctly
        str/isoformat: If you simply press enter, it will return the current date
        
    Raises
        Future date: If a future (invalid) date is entered, a message is displayed indicating that it is 
        not possible to enter future dates
        ValueError: If the entered date does not exist or the format is incorrect
    """
    
    while True:
        try:
            transaction_date = input(message)
            if transaction_date:
                object_date = datetime.strptime(transaction_date, "%Y-%m-%d").date()
                if object_date > date.today():
                    print("You cannot record future transactions")
                else:
                    final_date = object_date.isoformat()
                    return final_date
            else:
                final_date = date.today().isoformat()
                print("Today's date used")
                return final_date
        except ValueError:
            print("The date does not exist or the format is incorrect (use YYYY-MM-DD)")

def show_transactions(transactions):
    """
    List all the data specified above in the database
    
    Args:
        transactions (list): List with the respective data consulted in the database
        
    Returns:
        print: The data in the list is presented through a loop
        
    Raises
        There are no values: If there are no values in the list, it will simply indicate that they do not 
        exist and that you must create them before using this function
    """
    
    if len(transactions) != 0:
        for row in transactions:
            print(f"ID: {row[0]}, Date: {row[1]}, Concept: {row[2]}, Amount: {row[3]}, Category ID: {row[4]}")
    else:
        print("There are no transactions on this date")

def main():
    """
    Main entry point for the console version of MoneyWise
    
    Manages the program's main loop by displaying a menu with the following sections:
        - Categories (CRUD and Income/Expense type management)
        - Transactions (CRUD and date filters)
        - Dashboard (financial summary and charts)
        - Export tables to CSV or XLSX
        
    Each section has its own sub-loop that handles specific operations until the user decides to return 
    to the main menu
    
    Returns:
        None
    """
    
    # ================================
    # Main loop of the program
    # ================================
    while True:
        print("\n"+"="*60)
        print("  MONEY WISE - MANAGE YOUR MONEY")
        print("="*60)
        
        print("\n"+"-"*40)
        print("Menu:")
        print("-"*40+"\n")
        
        print("1. Categories")
        print("2. Transactions")
        print("3. Dashboard")
        print("4. Export tables")
        print("5. Exit")
        
        option_menu = validation_range("Choose an option: ", 1, 5)
        # ------------------------------
        # SECTION: CATEGORIES
        # ------------------------------
        if option_menu == 1:
            while True:
                print("\n"+"-"*40)
                print("Categories tab")
                print("-"*40+"\n")
                
                print("Description: This section will display all your existing tags/categories, classified as 'Income' or 'Expense'\n")
                
                dbc = DataBaseCategories()
                if len(dbc.check_data(0)) ==  0:
                    print("There are no categories, create one to get started")
                else:
                    print("List of categories")
                    for row in dbc.check_data(0):
                        print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")
                        
                print("\n1. Create a category")
                print("2. Edit a category")
                print("3. Delete a category")
                print("4. Exit the Categories tab")
                option_category_section = validation_range("Choose an option: ", 1, 4)
                # Option to create categories------------------------------------------------------------
                if option_category_section == 1:
                    category_name = input("\nEnter the category name: ")
                    category_type = validation_range("Enter the category type (1. Income - 2. Expense): ", 1, 2)
                    if category_type == 1:
                        category_type = "Income"
                    else:
                        category_type = "Expense"
                        
                    try:
                        new_category = Category(category_name, category_type)
                        dbc.insert_values(new_category)
                        print("\nCategory created successfully")
                        print("-"*40)
                    except Exception as e:
                        print(e)
                # Option to edit categories--------------------------------------------------------------
                elif option_category_section == 2:
                    if len(dbc.check_data(0)) ==  0:
                        print("\nThere are no categories, create one to get started")
                    else:
                        print("\nList of categories")
                        for row in dbc.check_data(0):
                            print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")
                        category_id = validation_id("Enter the ID of the category to update: ", dbc.consult_id())
                        actual_category = dbc.check_data(category_id)
                        new_category_name = input(f"Actual name ({actual_category[0][0]}): ")
                        if not new_category_name:
                            print("The name was not updated")
                        else:
                            dbc.update_values(0, new_category_name, category_id)
                            
                        new_category_type = validation_edit_values(f"Actual type ({actual_category[0][1]}), enter: 1. Income - 2. Expense: ", [1, 2])
                        if new_category_type:
                            if new_category_type == 1:
                                new_category_type = "Income"
                            else:
                                new_category_type = "Expense"
                            try:
                                dbc.update_values(1, new_category_type, category_id)
                            except Exception as e:
                                print(e)
                            print("\nOperation completed successfully")
                            print("-"*40)
                        else:
                            print("The type was not updated")
                            print("\nOperation completed successfully")
                            print("-"*40)
                # Option to delete categories------------------------------------------------------------
                elif option_category_section == 3:
                    if len(dbc.check_data(0)) ==  0:
                        print("\nThere are no categories, create one to get started")
                    else:
                        print("\nList of categories")
                        for row in dbc.check_data(0):
                            print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")
                        category_id = validation_id("Enter the ID of the category to delete: ", dbc.consult_id())
                        dbc.delete_values(category_id)
                        print("\nCategory successfully deleted")
                        print("-"*40)
                # Option to exit categories--------------------------------------------------------------
                else:
                    print("\nExiting the categories tab")
                    print("-"*40+"\n")
                    break
        # ------------------------------
        # SECTION: TRANSACTIONS
        # ------------------------------
        elif option_menu == 2:
            while True:
                print("\n"+"-"*40)
                print("Transactions tab")
                print("-"*40+"\n")
                
                print("Description: This section will display all existing transactions, and you can filter to search for specific transactions\n")
                dbc = DataBaseCategories()
                dbt = DataBaseTransactions()
                if len(dbt.check_data(0)) ==  0:
                    print("There are no transactions, create one to get started")
                else:
                    print("List of transactions")
                    for row in dbt.check_data(0):
                        print(f"ID: {row[0]}, Date: {row[1]}, Concept: {row[2]}, Amount: {row[3]}, Category ID: {row[4]}")
                        
                print("\n1. Create a transaction")
                print("2. Edit a transaction")
                print("3. Delete a transaction")
                print("4. Filter transactions")
                print("5. Exit the transaction tab")
                option_transaction_section = validation_range("Choose an option: ", 1, 5)
                # Option to create transactions----------------------------------------------------------
                if option_transaction_section == 1:
                    if len(dbc.check_data(0)) ==  0:
                        print("\nThere are no categories, create one to get started")
                    else:
                        print("\nList of categories")
                        for row in dbc.check_data(0):
                            print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")
                        transaction_date = validation_date("Enter the date (YYYY-MM-DD) or Enter for today's date: ")
                        transaction_concept = input("Enter the transaction concept: ")
                        transaction_amount = validation_range("Enter the amount: ", 0.01, float("inf"))
                        transaction_category_id = validation_id("Enter the ID of the category it belongs to: ", dbc.consult_id())
                        transaction_category_id = dbc.check_data(transaction_category_id)[0][0]
                        try:
                            new_transaction = Transaction(transaction_date, transaction_concept, transaction_amount, transaction_category_id)
                            dbt.insert_values(new_transaction)
                            print("\nTransaction created successfully")
                            print("-"*40)
                        except Exception as e:
                            print(e)
                # Option to edit transactions------------------------------------------------------------
                elif option_transaction_section == 2:
                    if len(dbt.check_data(0)) ==  0:
                        print("\nThere are no transactions, create one to get started")
                    else:
                        print("\nList of transactions")
                        for row in dbt.check_data(0):
                            print(f"ID: {row[0]}, Date: {row[1]}, Concept: {row[2]}, Amount: {row[3]}, Category ID: {row[4]}")
                        transaction_id = validation_id("Enter the ID of the transaction to update: ", dbt.consult_id())
                        actual_transaction = dbt.check_data(transaction_id)
                        new_transaction_date = validation_date(f"Actual date ({actual_transaction[0][0]}): ")
                        dbt.update_values(0, new_transaction_date, transaction_id)
                        new_transaction_concept = input(f"Actual concept ({actual_transaction[0][1]}): ")
                        if not new_transaction_concept:
                            print("The concept was not updated")
                        else:
                            dbt.update_values(1, new_transaction_concept, transaction_id)
                        while True:
                            new_transaction_amount = input(f"Actual amount ({actual_transaction[0][2]}): ")
                            if new_transaction_amount.isdigit() and 0.01 <= float(new_transaction_amount) <= float("inf"):
                                new_transaction_amount = float(new_transaction_amount)
                                dbt.update_values(2, new_transaction_amount, transaction_id)
                                break
                            elif new_transaction_amount == "":
                                print("The Amount was not updated")
                                break
                            else:
                                print("Enter only numbers, not letters or symbols")
                        print("\nList of categories")
                        for row in dbc.check_data(0):
                            print(f"ID: {row[0]}, Name: {row[1]}, Type: {row[2]}")
                        while True:
                            new_transaction_category_id = input(f"Actual category ({actual_transaction[0][3]}): ")
                            if new_transaction_category_id.isdigit() and int(new_transaction_category_id) in dbc.consult_id():
                                new_transaction_category_id = int(new_transaction_category_id)
                                new_transaction_category_id = dbc.check_data(new_transaction_category_id)[0][0]
                                dbt.update_values(3, new_transaction_category_id, transaction_id)
                                print("\nOperation completed successfully")
                                print("-"*40)
                                break
                            elif new_transaction_category_id == "":
                                print("The category was not updated")
                                print("\nOperation completed successfully")
                                print("-"*40)
                                break
                            else:
                                print("Enter only numbers, and that it falls within the existing categories")
                # Option to delete transactions----------------------------------------------------------
                elif option_transaction_section == 3:
                    if len(dbt.check_data(0)) ==  0:
                        print("\nThere are no transactions, create one to get started")
                    else:
                        print("\nList of transactions")
                        for row in dbt.check_data(0):
                            print(f"ID: {row[0]}, Date: {row[1]}, Concept: {row[2]}, Amount: {row[3]}, Category ID: {row[4]}")
                        transaction_id = validation_id("Enter the ID of the transaction to delete: ", dbt.consult_id())
                        dbt.delete_values(transaction_id)
                        print("\nTransaction successfully deleted")
                        print("-"*40)
                # Option to filter transactions----------------------------------------------------------
                elif option_transaction_section == 4:
                    while True:
                        print("\nFilter list")
                        print("1. Today")
                        print("2. Last 7 days")
                        print("3. This month")
                        print("4. Previous Month")
                        print("5. This Year")
                        print("6. Personalizado")
                        print("7. Back")
                        option_filter_transactions = validation_range("Choose an option: ", 1, 7)
                        if 1 <= option_filter_transactions <= 5:
                            show_transactions(dbt.filter_transactions(option_filter_transactions))
                        elif option_filter_transactions == 6:
                            start_date = validation_date("Enter the start date for the range: ")
                            end_date = validation_date("Enter the end date for the range: ")
                            show_transactions(dbt.filter_transactions(option_filter_transactions, start_date, end_date))
                        else:
                            print("\nLeaving...")
                            print("-"*40)
                            break
                # Option to exit transactions------------------------------------------------------------
                else:
                    print("\nExiting the transactions tab")
                    print("-"*40+"\n")
                    break
        # ------------------------------
        # SECTION: DASHBOARD
        # ------------------------------
        elif option_menu == 3:
            while True:
                print("\n"+"-"*40)
                print("Dashboard tab")
                print("-"*40+"\n")
                
                print("Description: This section shows a summary of the activity with money and graphs\n")
                dbt = DataBaseTransactions()
                
                print("1. This month's summary")
                print("2. Summary of the previous month")
                print("3. Custom range")
                print("4. Back")
                option_dashboard_section = validation_range("Choose an option: ", 1, 4)
                # Option to generate a summary for this month--------------------------------------------
                if option_dashboard_section == 1:
                    Analyzer(dbt.filter_transactions(3))
                # Option to generate a summary of the previous month-------------------------------------
                elif option_dashboard_section == 2:
                    Analyzer(dbt.filter_transactions(4))
                # Option to generate a summary of the range preferred by the user------------------------
                elif option_dashboard_section == 3:
                    start_date = validation_date("Enter the start date for the range: ")
                    end_date = validation_date("Enter the end date for the range: ")
                    Analyzer(dbt.filter_transactions(6, start_date, end_date))
                # option to exit the dashboard-----------------------------------------------------------
                else:
                    print("\nExiting the dashboard tab")
                    print("-"*40+"\n")
                    break
        # ------------------------------
        # SECTION: EXPORT TABLES
        # ------------------------------
        elif option_menu == 4:
            while True:
                print("\n"+"-"*40)
                print("Export tables")
                print("-"*40+"\n")
                
                print("Description: In this section you can export the tables (Categories and Transactions) to CSV or XLSX format\n")
                dbc = DataBaseCategories()
                
                print("1. Export to CSV")
                print("2. Export to XLSX")
                print("3. Back")
                option_export_section = validation_range("Choose an option: ", 1, 3)
                # Option to export to CSV----------------------------------------------------------------
                if option_export_section == 1:
                    if len(dbc.check_data(0)) ==  0:
                        print("\nThere are no categories, create one to get started")
                    else:
                        try:
                            export_tables(1)
                            print("\nData exported successfully")
                            print("-"*40)
                        except Exception as e:
                            print(e)
                # Option to export to XLSX---------------------------------------------------------------
                elif option_export_section == 2:
                    if len(dbc.check_data(0)) ==  0:
                        print("\nThere are no categories, create one to get started")
                    else:
                        try:
                            export_tables(2)
                            print("\nData exported successfully")
                            print("-"*40)
                        except Exception as e:
                            print(e)
                # Exit the table export option-----------------------------------------------------------
                else:
                    print("\nExiting the Export tables tab")
                    print("-"*40+"\n")
                    break
        # Exit the program-------------------------------------------------------------------------------
        else:
            print("\nThank you for using MoneyWise")
            print("="*60)
            break

if __name__ == "__main__":
    main()