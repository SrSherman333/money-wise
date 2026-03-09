from src.core.database import DataBaseCategories, DataBaseTransactions
from src.core.models import Category, Transaction
from datetime import date, datetime

def validation_range(message, min_value, max_value):
    while True:
        try:
            value = int(input(message))
            if min_value <= value <= max_value:
                return value
            print(f"Choose one option from {min_value} and {max_value}")
        except ValueError:
            print("Enter a valid number")
            
def validation_id(message, list_id):
    while True:
        try:
            value = int(input(message))
            if value in list_id:
                return value
            print("Enter a valid index")
        except ValueError:
            print("Enter only numbers")
            
def validation_edit_values(message, list_id):
    while True:
        value = input(message)
        if value.isdigit() and int(value) in list_id:
            return value
        elif value == "":
            print("The type was not updated")
            return None
        else:
            print("Enter a valid index")
            
def validation_date(message):
    while True:
        try:
            transaction_date = input(message)
            if transaction_date:
                object_date = datetime.strptime(transaction_date, "%Y-%m-%d").date()
                final_date = object_date.isoformat()
                return final_date
            else:
                final_date = date.today().isoformat()
                print("Today's date used")
                return final_date
        except ValueError:
            print("The date does not exist or the format is incorrect (use YYYY-MM-DD)")

def main():
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
        print("4. Exit")
        
        option_menu = validation_range("Choose an option: ", 1, 4)
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
                            dbc.update_values(1, new_category_type, category_id)
                            print("\nOperation completed successfully")
                            print("-"*40)
                        else:
                            print("The type was not updated")
                            print("\nOperation completed successfully")
                            print("-"*40)
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
                else:
                    print("\nExiting the categories tab")
                    print("-"*40+"\n")
                    break
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
                        transaction_category_id = validation_range("Enter the ID of the category it belongs to: ", 1, len(dbc. check_data(0)))
                        transaction_category_id = dbc.check_data(transaction_category_id)[0][0]
                        try:
                            new_transaction = Transaction(transaction_date, transaction_concept, transaction_amount, transaction_category_id)
                            dbt.insert_values(new_transaction)
                            print("\nTransaction created successfully")
                            print("-"*40)
                        except Exception as e:
                            print(e)
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
        else:
            print("\nThank you for using MoneyWise")
            print("="*60)
            break
    
if __name__ == "__main__":
    main()