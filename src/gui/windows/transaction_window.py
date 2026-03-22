import customtkinter as ctk
import tkinter as tk
import pandas as pd
from src.gui.components.calendar import CTkDatePicker
from src.gui.components.tables import TableTransactions
from src.core.database import DataBaseCategories, DataBaseTransactions
from src.core.models import Category
from src.core.analyzer import Analyzer

class TransactionWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.dbc = DataBaseCategories()
        self.dbt = DataBaseTransactions()
        self.categories = [category[1] for category in self.dbc.check_data(0)]
        self.cat_id = None
        self.list_results_labels = []
        self.configure(fg_color = "#648a64")
        self.create_widgets()
        
    def create_widgets(self):
        # ------------------------------
        # SECTION: TABLE
        # ------------------------------
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.frm_table = ctk.CTkScrollableFrame(self, fg_color="#a6b985", bg_color="#648a64", width=860,
                                        scrollbar_button_color="#46685b", scrollbar_button_hover_color="#213435")
        self.frm_table.grid(row=0, column=0, sticky="nsew", padx=5, pady=(0,10))
        self.frm_table.columnconfigure(1, weight=1)
        
        def options_column_filter(choice):
            if choice == "Index":
                self.option_filter.configure(state="normal")
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(values=["==", ">", "<", ">=", "<="])
                self.option_filter.set("==")
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2, 3...")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "Date":
                self.option_filter.configure(state="normal")
                self.option_filter.configure(values=["Today", "Last 7 days", "This month", "Previous Month",
                                                "This Year", "Custom range"])
                self.option_filter.set("Today")
                self.entry_filter.configure(state="disabled")
            elif choice == "Concept":
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.set("")
                self.option_filter.configure(state="disabled")
                self.entry_filter.configure(placeholder_text="Enter the transaction description")
            elif choice == "Amount":
                self.option_filter.configure(state="normal")
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(values=["==", ">", "<", ">=", "<="])
                self.option_filter.set("==")
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2, 3...")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            else:
                self.option_filter.configure(state="normal")
                self.option_filter.configure(values=["Name", "Type"])
                self.option_filter.set("Name")
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Enter the category name")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.entry_filter.focus_set()
        
        column_filter_values = ["Index", "Date", "Concept", "Amount", "Category"]
        column_filter = ctk.CTkComboBox(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435",
                                        width=100, values=column_filter_values, command=options_column_filter)
        column_filter.grid(row=0, column=0, pady=10)
        
        search_text = ctk.StringVar()
        self.entry_filter = ctk.CTkEntry(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                placeholder_text="One option: 4 - Multiple options: 1, 2, 3...",
                                textvariable=search_text)
        self.entry_filter.grid(row=0, column=1, pady=10, sticky="snew")
        search_text.trace_add("write", lambda *args:self.execute_filter())
        
        def options_filter(choice=None):
            if choice == "==":
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2, 3...")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == ">":
                self.entry_filter.configure(placeholder_text="Values higher than the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "<":
                self.entry_filter.configure(placeholder_text="Values lower than the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == ">=":
                self.entry_filter.configure(placeholder_text="Values greater than or equal to the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "<=":
                self.entry_filter.configure(placeholder_text="Values less than or equal to the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            
            if choice == "Today":
                self.entry_filter.configure(state="disabled")
            elif choice == "Last 7 days":
                self.entry_filter.configure(state="disabled")
            elif choice == "This month":
                self.entry_filter.configure(state="disabled")
            elif choice == "Previous Month":
                self.entry_filter.configure(state="disabled")
            elif choice == "This Year":
                self.entry_filter.configure(state="disabled")
            elif choice == "Custom range":
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Example: 2026-03-01 - 2026-03-07 (Dates separated by a hyphen)")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
                
            if choice == "Name":
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Enter the category name")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.entry_filter.focus_set()
            elif choice == "Type":
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Income or Expense")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
        
        self.option_filter = ctk.CTkComboBox(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435",
                                        values=["==", ">", "<", ">=", "<="], command=options_filter)
        self.option_filter.grid(row=0, column=2, pady=10)
        
        total_data_transactions = self.dbt.check_data(0)
        self.table_transactions = TableTransactions(self.frm_table, total_data_transactions, parent_ref=self)
        self.table_transactions.grid(row=1, column=0, columnspan=3)
            
        # ------------------------------
        # SECTION: SURVEY
        # ------------------------------
        frm_edit_create_delete_transactions = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64",
                                                width=300, height=180)
        frm_edit_create_delete_transactions.grid(row=1, column=0, sticky="nsew", padx=5)
        
        self.lbl_title = ctk.CTkLabel(frm_edit_create_delete_transactions, text="Create", 
                                        fg_color="#46685b", text_color="#e1e3ac", corner_radius=20, 
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_title.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
        
        lbl_date = ctk.CTkLabel(frm_edit_create_delete_transactions, text="Date:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_date.place(relx=0.06, rely=0.35, anchor=tk.CENTER)
        
        calendar = CTkDatePicker(frm_edit_create_delete_transactions)
        calendar.place(relx=0.26, rely=0.35, anchor=tk.CENTER)
        calendar.set_date_format("%Y-%m-%d")
        
        lbl_concept = ctk.CTkLabel(frm_edit_create_delete_transactions, text="Concept:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_concept.place(relx=0.06, rely=0.65, anchor=tk.CENTER)
        
        self.txtbox_concept = ctk.CTkTextbox(frm_edit_create_delete_transactions, font=ctk.CTkFont(size=13, weight="bold"),
                                width=200, height=80)
        self.txtbox_concept.place(relx=0.24, rely=0.7, anchor=tk.CENTER)
        
        lbl_amount = ctk.CTkLabel(frm_edit_create_delete_transactions, text="Amount:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_amount.place(relx=0.55, rely=0.4, anchor=tk.CENTER)
        
        self.entry_amount = ctk.CTkEntry(frm_edit_create_delete_transactions, font=ctk.CTkFont(size=13, weight="bold"),
                                placeholder_text="Example: 10.00", width=150)
        self.entry_amount.place(relx=0.7, rely=0.4, anchor=tk.CENTER)
        
        lbl_category = ctk.CTkLabel(frm_edit_create_delete_transactions, text="Category:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_category.place(relx=0.55, rely=0.7, anchor=tk.CENTER)
        
        cbbox_category = ctk.CTkComboBox(frm_edit_create_delete_transactions, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435", values=self.categories)
        cbbox_category.place(relx=0.7, rely=0.7, anchor=tk.CENTER)
        
        self.btn_category = ctk.CTkButton(frm_edit_create_delete_transactions, text="Confirm", 
                                    font=ctk.CTkFont(size=13, weight="bold"), text_color="#46685b", 
                                    border_color="#46685b", fg_color="#a6b985", hover_color="#213435",
                                    border_width=2, command=self.create_edit_delete_category)
        self.btn_category.place(relx=0.9, rely=0.55, anchor=tk.CENTER)
        
    def execute_filter(self):
        actual_value = self.entry_filter.get()
        option_filter_value = self.option_filter.get()
        df = pd.read_sql_query("SELECT * FROM Transactions", self.dbt.connection)
        
        if option_filter_value == "==":
            if "," not in actual_value and actual_value.strip().isdigit():
                index = int(actual_value.strip())-1
                df_filtered = df.loc[index]
                values = tuple([value for value in df_filtered.values.tolist()])
                values = [(int(values[0]), values[1], values[2], float(values[3]), values[4])]
                self.refresh(values, index)
            elif actual_value == "":
                self.refresh(self.dbt.check_data(0))
            else:
                indexes = [int(index.strip())-1 for index in actual_value.split(",") if index.strip().isdigit()]
                df_filtered = df.iloc[indexes].values.tolist()
                table_data = [tuple(value) for value in df_filtered]
                self.refresh(table_data, indexes)
            
    def refresh(self, table_data, index=None):
        if self.table_transactions:
            self.table_transactions.destroy()
            self.table_transactions = TableTransactions(self.frm_table, table_data, self, index)
            self.table_transactions.grid(row=1, column=0, columnspan=3)
        
    def create_edit_delete_category(self):
        actual_state = self.lbl_title.cget("text")
        actual_data_categories = self.dbc.check_data(0)
        actual_data_transactions = [value[4] for value in self.dbt.check_data(0)]
        new_name = self.entry_name.get()
        new_category = self.smb_category.get()
        
        if actual_state == "Create":
            for name in actual_data_categories:
                if new_name.strip().lower() == name[1].strip().lower():
                    repeated = True
                    self.entry_name.delete(0, "end")
                    self.entry_name.configure(border_color="red", border_width=2)
                    self.entry_name.insert(0, "Error: Existing category")
                    self.btn_category.configure(state="disabled")
                    self.after(2000, lambda:self.entry_name.delete(0, "end"))
                    self.after(2000, lambda:self.entry_name.configure(border_width=0))
                    self.after(2000, lambda:self.btn_category.configure(state="normal"))
                    break
                else:
                    repeated = False
                    
            if new_name == "":
                self.entry_name.configure(border_color="red", border_width=2)
                self.entry_name.insert(0, "Error: Enter a name")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.entry_name.delete(0, "end"))
                self.after(2000, lambda:self.entry_name.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif repeated == True:
                pass
            else:
                self.dbc.insert_values(Category(new_name, new_category))
                self.refresh(self.dbt.check_data(0))
                self.information_labels(self.dbt.check_data(0))
        elif actual_state == "Edit":
            if new_name == "":
                self.entry_name.configure(border_color="red", border_width=2)
                self.entry_name.insert(0, "Error: Enter a name")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.entry_name.delete(0, "end"))
                self.after(2000, lambda:self.entry_name.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            else:
                self.dbc.update_values(0, new_name, self.cat_id)
                self.dbc.update_values(1, new_category, self.cat_id)
                self.refresh(self.dbt.check_data(0))
                self.information_labels(self.dbt.check_data(0))
                self.lbl_title.configure(text="Create")
                self.entry_name.delete(0, "end")
                self.entry_name.focus()
                self.smb_category.set("Income")
        else:
            if self.entry_name.get() in actual_data_transactions:
                self.entry_name.configure(state="normal")
                self.entry_name.delete(0, "end")
                self.entry_name.configure(border_color="red", border_width=2)
                self.entry_name.insert(0, "Error: Category in use")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.entry_name.delete(0, "end"))
                self.after(2000, lambda:self.entry_name.insert(0, new_name))
                self.after(2000, lambda:self.entry_name.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
                self.after(2000, lambda:self.entry_name.configure(state="disabled"))
            else:
                self.entry_name.configure(state="normal")
                self.smb_category.configure(state="normal")
                self.dbc.delete_values(self.cat_id)
                self.refresh(self.dbt.check_data(0))
                self.information_labels(self.dbt.check_data(0))
                self.lbl_title.configure(text="Create")
                self.entry_name.delete(0, "end")
                self.entry_name.focus()
                self.smb_category.set("Income")