"""
Calculations for the dashboard.

Generates a summary of money handling based on the chosen option (This month, previous month, custom range), 
calculations, and graph creation

- DataBasedf_categories: Class to handle the data in the df_categories table
- matplotlib.pyplot: To generate the 3 corresponding graphs
- numpy: To calculate the list of colors in bar and pie charts
"""

from matplotlib.backends.backend_agg import FigureCanvasAgg
from src.core.database import DataBaseCategories
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
dbc = DataBaseCategories()

class Analyzer():
    """
    Class responsible for summarizing the money
    """
    
    def __init__(self, df_transactions, df_categories):
        """
        Definition of variables and lists to perform the calculations
        
        Args:
            df_transactions: List with the selected data (This month, Previous month, Custom range)
            
        Returns:
            None
        """
        self.df_transactions = df_transactions
        self.df_categories = df_categories
        self.df_complete = pd.merge(df_transactions, df_categories, left_on="Category_ID", right_on="Name", how="left")
        self.list_income = []
        self.list_expense = []
        self.total_incomes = 0
        self.total_expenses = 0
        self.percentage_savings = 0
        self.top_expenses = self.df_complete[self.df_complete["Category"]=="Expense"].nlargest(5, "Amount")
        self.calculate()
        
    def calculate(self):
        """
        Method that performs all calculations and stores the results
        in attributes, it does not print anything
        """
        self.total_incomes = self.df_complete[self.df_complete["Category"]=="Income"]["Amount"].sum()
        self.total_expenses = self.df_complete[self.df_complete["Category"]=="Expense"]["Amount"].sum()
        self.current_balance = self.total_incomes - self.total_expenses
        self.percentage_savings = (self.current_balance/self.total_incomes)*100
        
    def total_incomes_chart(self):
        plt.figure(figsize=(1.8, 1.8))
        values = [self.total_incomes, self.total_expenses]
        colors = ["#88B04B", "#B3C397"]
        plt.pie(values, colors=colors,wedgeprops={'width': 0.3})
        plt.axis("equal")
        ax = plt.gca()
        percentage = (self.total_incomes / (self.total_incomes + self.total_expenses)) * 100
        ax.text(0, 0, f"{percentage:.2f}%", ha='center', va='center', fontsize=10, fontweight='bold', color="#213435")
        plt.tight_layout()
        fig = plt.gcf()
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        return fig

    def total_expenses_chart(self):
        plt.figure(figsize=(1.8, 1.8))
        values = [self.total_incomes, self.total_expenses]
        colors = ["#B3C397", "#BC6C25"]
        plt.pie(values, colors=colors, wedgeprops={'width': 0.3})
        plt.axis("equal")
        ax = plt.gca()
        percentage = (self.total_expenses / (self.total_incomes + self.total_expenses)) * 100
        ax.text(0, 0, f"{percentage:.2f}%", ha='center', va='center', fontsize=10, fontweight='bold', color="#213435")
        plt.tight_layout()
        fig = plt.gcf()
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        return fig

    def percentage_saving_chart(self):
        plt.figure(figsize=(1.8, 1.8))
        values = [self.current_balance, self.total_incomes]
        colors = ["#648a64", "#B3C397"]
        plt.pie(values, colors=colors, wedgeprops={'width': 0.3})
        plt.axis("equal")
        ax = plt.gca()
        ax.text(0, 0, f"{self.percentage_savings:.2f}%", ha='center', va='center', fontsize=10, fontweight='bold', color="#213435")
        plt.tight_layout()
        fig = plt.gcf()
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        return fig

    def pie_chart(self):
        plt.figure(figsize=(2.9, 2))
        labels = []
        values = []
        for i in self.top_expenses.values.tolist():
            labels.append(i[4])
            values.append(i[3])
        colors = plt.cm.Greens(np.linspace(0.3, 0.8, len(labels)))
        desfase = [0.1]
        desfase.append([0 for i in range(len(self.top_expenses)-1)])
        desfase_unit = [item for sublist in desfase for item in (sublist if isinstance(sublist, list) else [sublist])]
        plt.pie(values, labels=labels, autopct='%2.2f%%', colors=colors, explode=desfase_unit, startangle=90, 
            textprops={'fontsize': 8, 'fontweight':'bold', 'color':'#213435'})
        plt.tight_layout()
        ax = plt.gca()
        fig = plt.gcf()
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        return fig

    def line_chart(self):
        plt.figure(figsize=(6, 2.4))
        df_line_chart = self.df_complete
        df_line_chart["Amount"] = np.where(self.df_complete["Category"]=="Expense", -self.df_complete["Amount"], self.df_complete["Amount"])
        df_transactions_ordened = sorted(df_line_chart.values.tolist(), key=lambda x: x[1])
        x_axis = []
        y_axis = []
        for i in df_transactions_ordened:
            x_axis.append(i[1])
            y_axis.append(i[3])
        plt.plot(x_axis, y_axis, marker="o", linewidth=2, markersize=8, color="steelblue")
        plt.fill_between(x_axis, y_axis, alpha=0.3, color="steelblue")
        plt.tick_params(axis='both', which='both', length=0)
        plt.tight_layout()
        plt.xticks(fontsize=8, fontweight='bold', color='#213435')
        plt.yticks(fontsize=8, fontweight='bold', color='#213435')
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(False)
        fig = plt.gcf()
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        return fig

    def section_numeric_summary(self):
        """
        Method that prints the numerical summary using the already calculated attributes
        """
        
        print("\nNumerical Summary")
        print(f"Total Incomes: {self.total_incomes:.2f}$")
        print(f"Total Expenses: {self.total_expenses:.2f}$")
        print(f"Current Balances: {self.current_balance:.2f}$")
        self.section_category_analysis()
        
    def section_category_analysis(self):
        """
        Second section of the dashboard summary, showing information regarding expenses and savings
        
        Args:
            Use variables and lists that were previously defined
            
        Returns:
            print: Top expenses
            print: Percentage of savingss
        """
        
        print("\nTop Expenses")
        for i, value in enumerate(self.top_expenses.values.tolist()):
            print(f"{i+1}. {value[4]} {value[3]:.2f}$")
            
        print(f"\nPercentage of Savings: {self.percentage_savings:.2f}%")
        self.section_graphs()
        
    def section_graphs(self):
        """
        Third section of the dashboard summary, here 3 graphs are created that detail expenses, 
        comparison and evolution of money. In addition to automatically saving the graphics in .png files
        
        Args:
            Use variables and lists that were previously defined
            
        Returns:
            Pie chart: Chart showing the distribution of expenses to compare where the most was spent
            Bar chart: A chart showing a comparison of expenses and income, indicating if the current 
                        balance is negative.
            Line chart: A graph showing the evolution of transactions with their respective dates, 
                        to analyze when more or less was spent
        """
        
        while True:
            option_graphs = input("\nGenerate graphs? yes/no: ")
            if option_graphs.lower() == "yes":
                print("Generating graphs...")
                # ================================
                # Pie chart
                # ================================
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
                plt.savefig("pie_chart.png", dpi=150)
                print("✓ Pie chart saved as 'pie_chart.png'")
                
                # ================================
                # Bar chart
                # ================================
                plt.figure(figsize=(10, 5))
                labels = ["Expenses", "Income"]
                values = [self.total_expenses, self.total_incomes]
                colors = plt.cm.tab10(np.linspace(0, 1, 2))
                bars = plt.bar(labels, values, color=colors, edgecolor="black")
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f"{height:.2f}$", ha="center", va="bottom", fontweight="bold")
                if self.current_balance < 0:
                    plt.text(0.5, self.total_expenses * 0.9, f"Less income than expenses (Current balance: {self.current_balance:.2f}$)",
                            fontsize=12, color="red", ha="center", bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
                plt.suptitle("Comparison of Expenses vs Income", fontsize=14, y=0.98)
                plt.title(f"Current Balance: {self.current_balance:.2f}$")
                plt.xlabel("Expenses and Income", fontsize=12)
                plt.ylabel("Money used", fontsize=12)
                plt.grid(True, alpha=0.3, axis="y")
                plt.tight_layout()
                plt.savefig("bar_chart.png", dpi=150)
                print("✓ Bar chart saved as 'bar_chart.png'")
                
                # ================================
                # Line chart
                # ================================
                plt.figure(figsize=(10, 5))
                df_transactions_ordened = sorted(self.df_transactions, key=lambda x: x[1])
                x_axis = []
                y_axis = []
                for i in df_transactions_ordened:
                    x_axis.append(i[1])
                    y_axis.append(i[3])
                plt.plot(x_axis, y_axis, marker="o", linewidth=2, markersize=8, color="steelblue",
                        label="Accumulated Balance")
                plt.fill_between(x_axis, y_axis, alpha=0.3, color="steelblue")
                plt.suptitle("Evolution of Transactions", fontsize=14, y=0.98)
                plt.xlabel("Elapsed dates")
                plt.ylabel("Money")
                plt.xticks(x_axis)
                plt.grid(True, alpha=0.3)
                plt.legend()
                plt.tight_layout()
                plt.savefig("line_chart.png", dpi=150)
                print("✓ Line chart saved as 'line_chart.png'")
                
                plt.show()
                
                print("\nSuccessfully completed summary")
                print("-"*40)
                break
            else:
                print("\nSuccessfully completed summary")
                print("-"*40)