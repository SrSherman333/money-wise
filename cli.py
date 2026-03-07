from src.core.database import DataBase
from src.core.models import Category

def validation(message, min_value, max_value):
    while True:
        try:
            value = int(input(message))
            if min_value <= value <= max_value:
                return value
            print(f"Choose one option from {min_value} and {max_value}")
        except ValueError:
            print("Enter a valid number")

def main():
    while True:
        print("="*60)
        print("  MONEY WISE - MANAGE YOUR MONEY")
        print("="*60)
        
        print("\nMenu:")
        print("-"*40+"\n")
        
        print("1. Categories")
        print("2. Transactions")
        print("3. Dashboard")
        print("4. Exit")
        
        option_menu = validation("Choose an option: ", 1, 4)
        if option_menu == 1:
            while True:
                print("\n"+"-"*40)
                print("Categories tab")
                print("-"*40+"\n")
                
                print("Description: This section will display all your existing tags/categories, classified as 'Income' or 'Expense'\n")
                
                db = DataBase()
                if len(db.check_data(0)) ==  0:
                    print("There are no categories, create one to get started")
                else:
                    print("List of categories")
                    for row in db.check_data(0):
                        print(f"{row[0]}. Name: {row[1]}, Type: {row[2]}")
                        
                print("\n1. Create a category")
                print("2. Edit a category")
                print("3. Delete a category")
                print("4. Exit the Categories tab")

                option_category_section = validation("Choose an option: ", 1, 4)
                if option_category_section == 1:
                    category_name = input("\nEnter the category name: ")
                    category_type = validation("Enter the category type (1. Income - 2. Expense): ", 1, 2)
                    if category_type == 1:
                        category_type = "Income"
                    else:
                        category_type = "Expense"
                        
                    try:
                        new_category = Category(category_name, category_type)
                        db.insert_values(new_category)
                        print("\nCategory created successfully")
                        print("-"*40)
                    except Exception as e:
                        print(e)
                elif option_category_section == 2:
                    if len(db.check_data(0)) ==  0:
                        print("\nThere are no categories, create one to get started")
                    else:
                        print("\nList of categories")
                        for row in db.check_data(0):
                            print(f"{row[0]}. Name: {row[1]}, Type: {row[2]}")
                        category_id = validation("Enter the ID of the category to update: ", 1, len(db.check_data(0)))
                        actual_category = db.check_data(category_id)
                        new_category_name = input(f"Actual name ({actual_category[0][0]}): ")
                        if not new_category_name:
                            print("The name was not updated")
                            pass
                        else:
                            db.update_values(0, new_category_name, category_id)
                            
                        while True:
                            new_category_type = input(f"Actual type ({actual_category[0][1]}), enter: 1. Income - 2. Expense: ")
                            if new_category_type.isdigit() and int(new_category_type) in (1, 2):
                                new_category_type = int(new_category_type)
                                if new_category_type == 1:
                                    new_category_type = "Income"
                                else:
                                    new_category_type = "Expense"
                                db.update_values(1, new_category_type, category_id)
                                print("\nOperation completed successfully")
                                print("-"*40)
                                break
                            elif new_category_type == "":
                                print("The type was not updated")
                                print("\nOperation completed successfully")
                                print("-"*40)
                                break
                            else:
                                print("Enter only numbers, and only 1 and 2")
                else:
                    break
        else:
            break
    
if __name__ == "__main__":
    main()