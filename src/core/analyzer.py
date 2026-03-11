from src.core.database import DataBaseCategories
import matplotlib.pyplot as plt
import numpy as np
dbc = DataBaseCategories()

class Analyzer():
    def __init__(self, list_transactions):
        self.list_transactions = list_transactions
        self.list_income = []
        self.list_expense = []
        self.total_incomes = 0
        self.total_expenses = 0
        self.section_numeric_summary()
        
    def section_numeric_summary(self):
        categories = dbc.check_data(0)
        for transaction in self.list_transactions:
            for category in categories:
                if transaction[4] == category[1]:
                    if category[2] == "Income":
                        self.list_income.append(transaction)
                    else:
                        self.list_expense.append(transaction)
                        
        print("\nNumerical Summary")
        for i in self.list_income:
            self.total_incomes += i[3]
        print(f"Total Incomes: {self.total_incomes:.2f}$")
        
        for i in self.list_expense:
            self.total_expenses += i[3]
        print(f"Total Expenses: {self.total_expenses:.2f}$")
        
        self.current_balance = self.total_incomes - self.total_expenses
        print(f"Current Balances: {self.current_balance:.2f}$")
        self.section_category_analysis()
        
    def section_category_analysis(self):
        print("\nTop Expenses")
        self.list_expenses_ordened = sorted(self.list_expense, key=lambda x: x[3], reverse=True)
        for i, value in enumerate(self.list_expenses_ordened):
            print(f"{i+1}. {value[4]} {value[3]:.2f}$")
            
        print(f"\nPercentage of Savings: {(self.current_balance/self.total_incomes)*100:.2f}%")
        self.section_graphs()
        
    def section_graphs(self):
        while True:
            option_graphs = input("Generate graphs? yes/no: ")
            if option_graphs.lower() == "yes":
                print("Generating graphs...")
                plt.figure(figsize=(10, 5))
                labels = []
                values = []
                for i in self.list_expenses_ordened:
                    labels.append(i[4])
                    values.append(i[3])
                colors = plt.cm.tab10(np.linspace(0, 1, len(labels)))
                desfase = [0.1]
                desfase.append([0 for i in range(len(self.list_expenses_ordened)-1)])
                desfase_unit = [item for sublist in desfase for item in (sublist if isinstance(sublist, list) else [sublist])]
                plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, explode=desfase_unit, startangle=90)
                plt.suptitle("Distribution of Expenses", fontsize=14, y=0.98)
                plt.title(f"Total Expenses: {self.total_expenses:.2f}$", fontsize=10, style='italic')
                plt.axis("equal")
                plt.legend()
                plt.tight_layout()
                plt.savefig("pie chart.png", dpi=150)
                print("✓ Pie chart saved as 'pie chart.png'")
                plt.show()
            else:
                pass