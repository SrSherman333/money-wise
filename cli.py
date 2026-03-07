from src.core.database import DataBase

def main():
    my_db = DataBase()
    while True:
        print("="*60)
        print("  MONEY WISE - MANAGE YOUR MONEY")
        print("="*60)
        
        print("\nChoose an option:")
        print("-"*40+"\n")
        
        print("1. Categories")
        print("2. Transactions")
        print("3. Dashboard")
        print("4. Exit")
        
        option_menu = input("Option (1, 2, 3, 4): ")
        
        if option_menu == "1":
            print("\nCategories tab")
            print("-"*40+"\n")
            
            print("Description: This section will display all your existing tags/categories, classified as 'Income' or 'Expense'\n")
            
            db = DataBase()
            if len(db.data) ==  0:
                print("There are no categories, create one to get started")
            else:
                for row in db.data:
                    print(row)
                    
            while True:
                print("\n1. Create a category")
                print("2. Edit a category")
                print("3. Delete a category")
                print("4. Exit the Categories section")

                option_category_section = input("Choose an option: ")
                if option_category_section == "1":
                    category_name = input("\nEnter the category name: ")
                    while True:
                        try:
                            category_type = int(input("Enter the category type (1. Income/2. Expense): "))
                            if not 1 <= category_type <= 2:
                                print("Enter only one of the 2 options (1, 2)")
                            else:
                                if category_type == 1:
                                    category_type = "Income"
                                else:
                                    category_type = "Expense"
                                    
                                try:
                                    my_db.insert_values(category_name, category_type)
                                    print("\nCategory created successfully")
                                    print("-"*40)
                                    break
                                except Exception as e:
                                    print(e)
                        except Exception:
                            print("Enter only one of the 2 options (1, 2)")
                else:
                    break
        else:
            break
    
if __name__ == "__main__":
    main()