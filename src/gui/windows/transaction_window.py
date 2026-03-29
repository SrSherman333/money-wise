import customtkinter as ctk
import tkinter as tk
import pandas as pd
from datetime import *
from src.gui.components.calendar import CTkDatePicker
from src.gui.components.tables import TableTransactions
from src.core.database import DataBaseCategories, DataBaseTransactions
from src.core.models import Transaction
from src.core.analyzer import Analyzer

class TransactionWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.dbc = DataBaseCategories()
        self.dbt = DataBaseTransactions()
        self.cat_id = None
        self.list_results_labels = []
        self.configure(fg_color = "#648a64")
        
        self.load_data()
        
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
            dataframe = [tuple(value) for value in self.data.values.tolist()]
            if choice == "Index":
                self.refresh(dataframe)
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
                today = date.today().isoformat()
                self.entry_filter.insert(0, today)
                self.entry_filter.configure(state="disabled")
                df_filtered = self.data[self.data["Date"] == today]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif choice == "Concept":
                self.refresh(dataframe)
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.set("")
                self.option_filter.configure(state="disabled")
                self.entry_filter.configure(placeholder_text="Enter the transaction description")
            elif choice == "Amount":
                self.refresh(dataframe)
                self.option_filter.configure(state="normal")
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(values=["==", ">", "<", ">=", "<="])
                self.option_filter.set("==")
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2, 3...")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            else:
                self.refresh(dataframe)
                self.option_filter.configure(state="normal")
                self.option_filter.configure(values=["Name", "Type"])
                self.option_filter.set("Name")
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Enter the category name")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
        
        column_filter_values = ["Index", "Date", "Concept", "Amount", "Category"]
        self.column_filter = ctk.CTkComboBox(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435",
                                        width=100, values=column_filter_values, command=options_column_filter)
        self.column_filter.grid(row=0, column=0, pady=10)
        
        self.entry_filter = ctk.CTkEntry(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                placeholder_text="One option: 4 - Multiple options: 1, 2, 3...",)
        self.entry_filter.grid(row=0, column=1, pady=10, sticky="snew")
        self.entry_filter.bind("<KeyRelease>", self.execute_filter)
        
        def options_filter(choice):
            dataframe = [tuple(value) for value in self.data.values.tolist()]
            if choice == "==":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2, 3...")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == ">":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values higher than the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "<":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values lower than the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == ">=":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values greater than or equal to the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "<=":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values less than or equal to the entered number will be filtered out")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            
            self.today = date.today()
            if choice == "Today":
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.entry_filter.insert(0, self.today.isoformat())
                self.entry_filter.configure(state="disabled")
                df_filtered = self.data[self.data["Date"] == self.today]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif choice == "Last 7 days":
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                seven_days_ago = self.today.replace(day=self.today.day - 6)
                self.entry_filter.insert(0, f"{seven_days_ago.isoformat()} - {self.today.isoformat()}")
                self.entry_filter.configure(state="disabled")
                df_filtered = self.data[self.data["Date"] >= seven_days_ago.isoformat()]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif choice == "This month":
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                first_day_month = self.today.replace(day = 1)
                self.entry_filter.insert(0, f"{first_day_month.isoformat()} - {self.today.isoformat()}")
                self.entry_filter.configure(state="disabled")
                df_filtered = self.data[self.data["Date"] >= first_day_month.isoformat()]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif choice == "Previous Month":
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                first_day_month = self.today.replace(day=1)
                first_day_previous_month = first_day_month.replace(month=self.today.month-1)
                last_day_previous_month = first_day_month - timedelta(days=1)
                self.entry_filter.insert(0, f"{first_day_previous_month.isoformat()} - {last_day_previous_month.isoformat()}")
                self.entry_filter.configure(state="disabled")
                df_filtered = self.data[(self.data["Date"] >= first_day_previous_month.isoformat()) & (self.data["Date"] <= last_day_previous_month.isoformat())]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif choice == "This Year":
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                first_day_year = self.today.replace(month=1, day=1)
                self.entry_filter.insert(0, f"{first_day_year.isoformat()} - {self.today.isoformat()}")
                self.entry_filter.configure(state="disabled")
                df_filtered = self.data[self.data["Date"]>=first_day_year.isoformat()]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif choice == "Custom range":
                self.refresh(dataframe)
                self.entry_filter.configure(state="normal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.entry_filter.configure(placeholder_text="Example: 2026-03-01 to 2026-03-07 (Dates separated by 'to')")
                self.option_filter.focus_set()
                
            if choice == "Name":
                self.refresh(dataframe)
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Enter the category name")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "Type":
                self.refresh(dataframe)
                self.entry_filter.configure(state="normal")
                self.entry_filter.configure(placeholder_text="Income or Expense")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
        
        self.option_filter = ctk.CTkComboBox(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435",
                                        values=["==", ">", "<", ">=", "<="], command=options_filter)
        self.option_filter.grid(row=0, column=2, pady=10)
        
        self.table_transactions = TableTransactions(self.frm_table, [tuple(value) for value in self.data.values.tolist()], parent_ref=self)
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
        
        self.calendar = CTkDatePicker(frm_edit_create_delete_transactions)
        self.calendar.place(relx=0.26, rely=0.35, anchor=tk.CENTER)
        self.calendar.set_date_format("%Y-%m-%d")
        
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
        lbl_amount.place(relx=0.48, rely=0.4, anchor=tk.CENTER)
        
        self.entry_amount = ctk.CTkEntry(frm_edit_create_delete_transactions, font=ctk.CTkFont(size=13, weight="bold"),
                                placeholder_text="Example: 10.00", width=150)
        self.entry_amount.place(relx=0.63, rely=0.4, anchor=tk.CENTER)
        self.entry_amount.bind("<KeyRelease>", self.amount_control)
        
        lbl_category = ctk.CTkLabel(frm_edit_create_delete_transactions, text="Category:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_category.place(relx=0.48, rely=0.7, anchor=tk.CENTER)
        
        def option_cbbox_category(choice):
            self.entry_amount.configure(border_width=2, border_color=self.colors_cells[choice][0])
            self.cbbox_category.configure(border_width=2, border_color=self.colors_cells[choice][0])
            self.amount_control()
        
        self.cbbox_category = ctk.CTkComboBox(frm_edit_create_delete_transactions, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435", values=self.categories_names,
                                        command=option_cbbox_category)
        self.cbbox_category.place(relx=0.63, rely=0.7, anchor=tk.CENTER)
        
        self.entry_amount.configure(border_width=2, border_color=self.colors_cells[self.cbbox_category.get()][0])
        self.cbbox_category.configure(border_width=2, border_color=self.colors_cells[self.cbbox_category.get()][0])
        
        self.lbl_curent_balance = ctk.CTkLabel(frm_edit_create_delete_transactions, text=f"Current Balance: {self.current_balance:.2f}$", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, font=ctk.CTkFont(size=13, weight="bold"),
                                width=200, wraplength=200)
        self.lbl_curent_balance.place(relx=0.87, rely=0.4, anchor=tk.CENTER)
        
        self.load_table_data()
        
        self.btn_category = ctk.CTkButton(frm_edit_create_delete_transactions, text="Confirm", 
                                    font=ctk.CTkFont(size=13, weight="bold"), text_color="#46685b", 
                                    border_color="#46685b", fg_color="#a6b985", hover_color="#213435",
                                    border_width=2, command=self.create_edit_delete_category)
        self.btn_category.place(relx=0.87, rely=0.7, anchor=tk.CENTER)
        
    def execute_filter(self, event):
        actual_value = self.entry_filter.get()
        option_filter_value = self.option_filter.get()
        column_filter_value = self.column_filter.get()
        dataframe = [tuple(value) for value in self.data.values.tolist()]
        if self.data["Amount"].dtype == "float64":
            dataframe = [tuple(value) for value in self.data.values.tolist()]
            dataframe = [(value[0], value[1], value[2], f"{value[3]:.2f}", value[4]) for value in dataframe]
        
        if option_filter_value == "==" and column_filter_value == "Index":
            if "," not in actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                index = int(actual_value.strip())-1
                try:
                    df_filtered = self.data.loc[index]
                    values = tuple([value for value in df_filtered.values.tolist()])
                    values = [(int(values[0]), values[1], values[2], str(values[3]), values[4])]
                    self.refresh(values)
                except Exception:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif "," in actual_value:
                self.entry_filter.configure(border_width=0)
                indexes = [int(index.strip())-1 for index in actual_value.split(",") if index.strip().isdigit()]
                try:
                    df_filtered = self.data.iloc[indexes].drop_duplicates()
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    self.refresh(table_data)
                except Exception:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == ">" and column_filter_value == "Index":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.data[self.data.index > int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == "<" and column_filter_value == "Index":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.data[self.data.index < int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == ">=" and column_filter_value == "Index":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.data[self.data.index >= int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == "<=" and column_filter_value == "Index":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.data[self.data.index <= int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        
        if option_filter_value == "Custom range":
            if "to" in actual_value and actual_value.count("to")==1:
                dates = []
                for date in actual_value.split("to"):
                    if date:
                        try:
                            object_date = datetime.strptime(date.strip(), "%Y-%m-%d").date()
                            if object_date > self.today:
                                self.entry_filter.configure(border_width=2, border_color="red")
                            else:
                                self.entry_filter.configure(border_width=0)
                                dates.append(object_date.isoformat())
                        except Exception as e:
                            self.entry_filter.configure(border_width=2, border_color="red")
                    else:
                        pass
                if len(dates) == 2:
                    df_filtered = self.data[(self.data["Date"]>=dates[0]) & (self.data["Date"]<=dates[1])]
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
        
        if column_filter_value == "Concept":
            if actual_value:
                df_filtered = self.data[self.data["Concept"].str.contains(actual_value, case=False)]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            else:
                self.refresh(dataframe)
        
        if option_filter_value == "==" and column_filter_value == "Amount":
            if "," not in actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                amount = float(actual_value.strip())
                try:
                    df_filtered = self.df[self.df["Amount"]==amount]
                    table_data = [tuple([value[0], value[1], value[2], f"{value[3]:.2f}", value[4]]) for value in df_filtered.values.tolist()]
                    self.refresh(table_data)
                except Exception as e:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif "," in actual_value:
                self.entry_filter.configure(border_width=0)
                amounts = [int(index.strip()) for index in actual_value.split(",") if index.strip().isdigit()]
                try:
                    df_filtered = self.df[self.df["Amount"].isin(amounts)]
                    table_data = [tuple([value[0], value[1], value[2], f"{value[3]:.2f}", value[4]]) for value in df_filtered.values.tolist()]
                    self.refresh(table_data)
                except Exception as e:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == ">" and column_filter_value == "Amount":
            if actual_value:
                try:
                    float(actual_value.strip())
                    self.entry_filter.configure(border_width=0)
                    if self.data["Amount"].dtype != "float64":
                        self.data["Amount"] = [float(i.replace("$", "")) for i in self.data["Amount"].values.tolist()]
                    df_filtered = self.data[self.data["Amount"] > float(actual_value)]
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    table_data = [(value[0], value[1], value[2], f"{value[3]:.2f}", value[4]) for value in table_data]
                    self.refresh(table_data)
                except ValueError:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == "<" and column_filter_value == "Amount":
            if actual_value:
                try:
                    float(actual_value.strip())
                    self.entry_filter.configure(border_width=0)
                    if self.data["Amount"].dtype != "float64":
                        self.data["Amount"] = [float(i.replace("$", "")) for i in self.data["Amount"].values.tolist()]
                    df_filtered = self.data[self.data["Amount"] < float(actual_value)]
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    table_data = [(value[0], value[1], value[2], f"{value[3]:.2f}", value[4]) for value in table_data]
                    self.refresh(table_data)
                except ValueError:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == ">=" and column_filter_value == "Amount":
            if actual_value:
                try:
                    float(actual_value.strip())
                    self.entry_filter.configure(border_width=0)
                    if self.data["Amount"].dtype != "float64":
                        self.data["Amount"] = [float(i.replace("$", "")) for i in self.data["Amount"].values.tolist()]
                    df_filtered = self.data[self.data["Amount"] >= float(actual_value)]
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    table_data = [(value[0], value[1], value[2], f"{value[3]:.2f}", value[4]) for value in table_data]
                    self.refresh(table_data)
                except ValueError:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == "<=" and column_filter_value == "Amount":
            if actual_value:
                try:
                    float(actual_value.strip())
                    self.entry_filter.configure(border_width=0)
                    if self.data["Amount"].dtype != "float64":
                        self.data["Amount"] = [float(i.replace("$", "")) for i in self.data["Amount"].values.tolist()]
                    df_filtered = self.data[self.data["Amount"] <= float(actual_value)]
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    table_data = [(value[0], value[1], value[2], f"{value[3]:.2f}", value[4]) for value in table_data]
                    self.refresh(table_data)
                except ValueError:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
                
        if option_filter_value == "Name":
            if actual_value:
                df_filtered = self.data[self.data["Category_ID"].str.contains(actual_value, case=False)]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            else:
                self.refresh(dataframe)
        elif option_filter_value == "Type":
            if actual_value == "Expense":
                self.entry_filter.configure(border_width=0)
                if self.data["Amount"].dtype == "float64":
                    self.data["Amount"] = [tuple(value) for value in self.data.values.tolist()]
                    self.data["Amount"] = [(value[0], value[1], value[2], f"{value[3]:.2f}", value[4]) for value in dataframe]
                df_filtered = self.data[self.data["Amount"].str.startswith("-")]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "Income":
                self.entry_filter.configure(border_width=0)
                if self.data["Amount"].dtype == "float64":
                    self.data["Amount"] = [tuple(value) for value in self.data.values.tolist()]
                df_filtered = self.data[self.data["Amount"].str.startswith("+")]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
            
    def amount_control(self, event=None):
        actual_mode = self.lbl_title.cget("text")
        actual_value = self.entry_amount.get()
        color_categorie = self.colors_cells[self.cbbox_category.get()][0]
        
        def valid_number(value):
            try:
                value = float(value)
                return value if value > 0 else None
            except ValueError:
                return None
        
        if actual_value == "":
            self.entry_amount.configure(border_color=color_categorie)
            if self.current_balance >= 0:
                self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="#648a64")
            else:
                self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="orange")
            return
        
        amount = valid_number(actual_value)
        
        if actual_mode in ("Edit", "Delete"):
            if amount != None:
                if color_categorie == "#BC6C25":
                    amount = -amount
                else:
                    amount = abs(amount)
                self.amount_column_data[self.table_transactions.row_clicked-1] = amount
                current_balance = sum(i for i in self.amount_column_data)
                if current_balance >= 0:
                    self.entry_amount.configure(border_color=color_categorie)
                    self.lbl_curent_balance.configure(text=f"Current Balance: {current_balance:.2f}$", fg_color="#648a64")
                else:
                    self.entry_amount.configure(border_color=color_categorie)
                    self.lbl_curent_balance.configure(text=f"Current Balance: {current_balance:.2f}$", fg_color="orange")
            else:
                self.entry_amount.configure(border_color="red")
                if self.current_balance >= 0:
                    self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="#648a64")
                else:
                    self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="orange")
        else:
            if amount != None:
                if color_categorie=="#BC6C25":
                    current_balance = self.current_balance-amount
                else:
                    current_balance = self.current_balance+amount
                if current_balance >= 0:
                    self.entry_amount.configure(border_color=color_categorie)
                    self.lbl_curent_balance.configure(text=f"Current Balance: {current_balance:.2f}$", fg_color="#648a64")
                else:
                    self.entry_amount.configure(border_color=color_categorie)
                    self.lbl_curent_balance.configure(text=f"Current Balance: {current_balance:.2f}$", fg_color="orange")
            else:
                self.entry_amount.configure(border_color="red")
                if self.current_balance >= 0:
                    self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="#648a64")
                else:
                    self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="orange")
        
    def refresh(self, table_data):
        if self.table_transactions:
            self.table_transactions.destroy()
            self.table_transactions = TableTransactions(self.frm_table, table_data, self)
            self.table_transactions.grid(row=1, column=0, columnspan=3)
        
    def create_edit_delete_category(self):
        actual_state = self.lbl_title.cget("text")
        new_date = self.calendar.date_entry.get()
        new_concept = self.txtbox_concept.get("1.0", "end-1c")
        new_amount = self.entry_amount.get()
        new_category = self.cbbox_category.get()
        
        try:
            object_date = datetime.strptime(new_date, "%Y-%m-%d").date()
            if object_date > date.today():
                new_date = ""
            else:
                final_date = object_date.isoformat()
                new_date = final_date
        except ValueError:
            new_date = ""
        
        if actual_state == "Create":
            if new_date == "":
                self.calendar.date_entry.configure(border_color="red", border_width=2)
                self.calendar.date_entry.insert(0, "Error: Enter a Date")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.calendar.date_entry.delete(0, "end"))
                self.after(2000, lambda:self.calendar.date_entry.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif new_concept == "":
                self.txtbox_concept.configure(border_color="red", border_width=2)
                self.txtbox_concept.insert("0.0", "Error: Enter a Concept")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.txtbox_concept.delete("1.0", "end"))
                self.after(2000, lambda:self.txtbox_concept.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif new_amount == "" or self.entry_amount.cget("border_color")=="red":
                self.entry_amount.delete(0, "end")
                self.entry_amount.configure(border_color="red", border_width=2)
                self.entry_amount.insert(0, "Error: Enter a Amount")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.entry_amount.delete(0, "end"))
                self.after(2000, lambda:self.entry_amount.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif new_category not in self.categories_names:
                self.cbbox_category.configure(border_color="red", border_width=2)
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.cbbox_category.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            else:
                self.dbt.insert_values(Transaction(new_date, new_concept, new_amount, new_category))
                self.load_data()
                self.refresh([tuple(value) for value in self.data.values.tolist()])
                self.load_table_data()
                self.calendar.date_entry.delete(0, "end")
                self.txtbox_concept.delete("1.0", "end")
                self.entry_amount.delete(0, "end")
                self.calendar.date_entry.focus()
                self.cbbox_category.set(self.categories_names[0])
        elif actual_state == "Edit":
            if new_date == "":
                self.calendar.date_entry.configure(border_color="red", border_width=2)
                self.calendar.date_entry.insert(0, "Error: Enter a valid date")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.calendar.date_entry.delete(0, "end"))
                self.after(2000, lambda:self.calendar.date_entry.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif new_concept == "":
                self.txtbox_concept.configure(border_color="red", border_width=2)
                self.txtbox_concept.insert("0.0", "Error: Enter a Concept")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.txtbox_concept.delete("1.0", "end"))
                self.after(2000, lambda:self.txtbox_concept.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif new_amount == "" or self.entry_amount.cget("border_color")=="red":
                self.entry_amount.delete(0, "end")
                self.entry_amount.configure(border_color="red", border_width=2)
                self.entry_amount.insert(0, "Error: Enter a Amount")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.entry_amount.delete(0, "end"))
                self.after(2000, lambda:self.entry_amount.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            elif new_category not in self.categories_names:
                self.cbbox_category.configure(border_color="red", border_width=2)
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.cbbox_category.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
            else:
                self.dbt.update_values(0, new_date, self.cat_id)
                self.dbt.update_values(1, new_concept, self.cat_id)
                self.dbt.update_values(2, new_amount, self.cat_id)
                self.dbt.update_values(3, new_category, self.cat_id)
                self.load_data()
                self.refresh([tuple(value) for value in self.data.values.tolist()])
                self.load_table_data()
                self.lbl_title.configure(text="Create")
                self.calendar.date_entry.delete(0, "end")
                self.txtbox_concept.delete("1.0", "end")
                self.entry_amount.delete(0, "end")
                self.calendar.date_entry.focus()
                self.cbbox_category.set(self.categories_names[0])
        else:
            self.calendar.date_entry.configure(state="normal")
            self.txtbox_concept.configure(state="normal")
            self.entry_amount.configure(state="normal")
            self.cbbox_category.configure(state="normal")
            self.dbt.delete_values(self.cat_id)
            self.load_data()
            self.refresh([tuple(value) for value in self.data.values.tolist()])
            self.load_table_data()
            self.lbl_title.configure(text="Create")
            self.calendar.date_entry.delete(0, "end")
            self.txtbox_concept.delete("1.0", "end")
            self.entry_amount.delete(0, "end")
            self.calendar.date_entry.focus()
            self.cbbox_category.set(self.categories_names[0])
            
    def load_data(self):
        self.transactions = self.dbt.check_data(0)
        self.transactions = sorted(self.transactions, key=lambda x: datetime.strptime(x[1], '%Y-%m-%d'), reverse=True)
        self.categories = self.dbc.check_data(0)
        self.df = pd.DataFrame(self.transactions, columns=["Index", "Date", "Concept", "Amount", "Category_ID"])
        self.df = self.df.sort_values(by="Date", ascending=False).reset_index(drop=True)
        self.df["№"] = self.df.index + 1
        self.df = self.df[["№", "Date", "Concept", "Amount", "Category_ID"]]
        self.data = self.df[["№", "Date", "Concept", "Amount", "Category_ID"]]
        self.data["Amount"] = ["{:.2f}".format(i) for i in self.data["Amount"].values.tolist()]
        self.categories_names = [category[1] for category in self.categories]
        analyzer = Analyzer([tuple(value) for value in self.df.values.tolist()], self.categories)
        self.current_balance = analyzer.current_balance
        
        self.colors_cells = {}
        for category in self.categories:
            if category[2] == "Income":
                self.colors_cells[category[1]] = ("#88B04B", "+")
            else:
                self.colors_cells[category[1]] = ("#BC6C25", "-")
                
    def load_table_data(self):
        self.amount_column_data = self.table_transactions.get_column(3)
        del self.amount_column_data[0]
        self.data["Amount"] = self.amount_column_data
        
        self.amount_column_data = [float(amount.replace("$", "") ) for amount in self.amount_column_data]
        
        if self.current_balance >= 0:
            self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="#648a64")
        else:
            self.lbl_curent_balance.configure(text=f"Current Balance: {self.current_balance:.2f}$", fg_color="orange")