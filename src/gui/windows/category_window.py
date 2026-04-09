import customtkinter as ctk
import tkinter as tk
import pandas as pd
from src.gui.components.tables import TableCategories
from src.core.database import DataBaseCategories, DataBaseTransactions
from src.core.models import Category

class CategoryWindow(ctk.CTkFrame):
    def __init__(self, master, parent_ref):
        super().__init__(master)
        self.parent_ref = parent_ref
        self.dbc = DataBaseCategories()
        self.dbt = DataBaseTransactions()
        self.cat_id = None
        self.colors_cells = {"Nothing":("gray", "#")}
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
        
        self.frm_table = ctk.CTkScrollableFrame(self, fg_color="#a6b985", bg_color="#648a64", width=450,
                                        scrollbar_button_color="#46685b", scrollbar_button_hover_color="#213435")
        self.frm_table.grid(row=0, column=0, sticky="nsew", rowspan=2, padx=5)
        
        canvas = self.frm_table._parent_canvas
        
        self.scroll_active = False
        
        def on_enter(event):
            self.scroll_active = True
            
        def on_leave(event):
            self.scroll_active = False
            
        self.frm_table.bind("<Enter>", on_enter)
        self.frm_table.bind("<Leave>", on_leave)
        
        def on_mouse_wheel(event):
            if self.scroll_active:
                if event.num == 4 or (hasattr(event, "delta") and event.delta > 0):
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5 or (hasattr(event, "delta") and event.delta < 0):
                    canvas.yview_scroll(1, "units")
                    
        root = self.winfo_toplevel()
        root.bind("<MouseWheel>", on_mouse_wheel)
        root.bind("<Button-4>", on_mouse_wheel)
        root.bind("<Button-5>", on_mouse_wheel)
        
        def options_column_filter(choice):
            if choice == "Index":
                self.option_filter.configure(state="normal")
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(values=["==", ">", "<", ">=", "<="])
                self.option_filter.set("==")
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "Name":
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(values=[""])
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.set("")
                self.option_filter.configure(state="disabled")
                self.entry_filter.configure(placeholder_text="Enter the category name")
            else:
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(values=[""])
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.set("")
                self.option_filter.configure(state="disabled")
                self.entry_filter.configure(placeholder_text="Enter the category type")
        
        column_filter_values = ["Index", "Name", "Category"]
        self.column_filter = ctk.CTkComboBox(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435",
                                        values=column_filter_values, width=50, command=options_column_filter)
        self.column_filter.grid(row=0, column=0, pady=10, sticky="snew")
        
        self.entry_filter = ctk.CTkEntry(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                placeholder_text="One option: 4 - Multiple options: 1, 2", width=206)
        self.entry_filter.grid(row=0, column=1, pady=10, sticky="snew")
        self.entry_filter.bind("<KeyRelease>", self.execute_filter)
        
        def options_filter(choice):
            dataframe = [tuple(value) for value in self.df.values.tolist()]
            if choice == "==":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="One option: 4 - Multiple options: 1, 2")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == ">":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values higher than the index")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "<":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values lower than the index")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == ">=":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values greater than or equal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
            elif choice == "<=":
                self.refresh(dataframe)
                self.entry_filter.configure(placeholder_text="Values less than or equal")
                if self.entry_filter.get():
                    self.entry_filter.delete(0, "end")
                self.option_filter.focus_set()
        
        self.option_filter = ctk.CTkComboBox(self.frm_table, font=ctk.CTkFont(size=13, weight="bold"),
                                        button_color="#648a64", button_hover_color="#213435",
                                        values=["==", ">", "<", ">=", "<="], width=40, command=options_filter)
        self.option_filter.grid(row=0, column=2, pady=10, sticky="snew")
        
        if len(self.categories) > 0:
            self.column_filter.configure(state="normal")
            self.entry_filter.configure(state="normal")
            self.option_filter.configure(state="normal")
        else:
            self.column_filter.configure(state="disabled")
            self.entry_filter.configure(state="disabled")
            self.option_filter.configure(state="disabled")

        self.table_categories = TableCategories(self.frm_table, [tuple(value) for value in self.df.values.tolist()], parent_ref=self)
        self.table_categories.grid(row=1, column=0, columnspan=3)
            
        # ------------------------------
        # SECTION: SURVEY
        # ------------------------------
        frm_edit_create_categories = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64",
                                                width=400, height=150)
        frm_edit_create_categories.grid(row=0, column=1, sticky="nsew", padx=5)
        
        self.lbl_title = ctk.CTkLabel(frm_edit_create_categories, text="Create", 
                                        fg_color="#46685b", text_color="#e1e3ac", corner_radius=20, 
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_title.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
        
        lbl_name = ctk.CTkLabel(frm_edit_create_categories, text="Name:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_name.place(relx=0.20, rely=0.4, anchor=tk.CENTER)
        
        self.entry_name = ctk.CTkEntry(frm_edit_create_categories, font=ctk.CTkFont(size=13, weight="bold"),
                                placeholder_text="Example: Food", width=200)
        self.entry_name.place(relx=0.65, rely=0.4, anchor=tk.CENTER)
        
        lbl_category = ctk.CTkLabel(frm_edit_create_categories, text="Category:", fg_color="#648a64", 
                                text_color="#e1e3ac", corner_radius=20, 
                                font=ctk.CTkFont(size=13, weight="bold"))
        lbl_category.place(relx=0.20, rely=0.62, anchor=tk.CENTER)
        
        self.smb_category = ctk.CTkSegmentedButton(frm_edit_create_categories, values=["Income", "Expense"], 
                                        fg_color="#648a64", text_color="#46685b", corner_radius=20, 
                                        font=ctk.CTkFont(size=13, weight="bold"), selected_color="#213435",
                                        unselected_color="#a6b985", selected_hover_color="#213435",
                                        unselected_hover_color="#213435")
        self.smb_category.place(relx=0.65, rely=0.62, anchor=tk.CENTER)
        self.smb_category.set("Income")
        
        self.btn_category = ctk.CTkButton(frm_edit_create_categories, text="Confirm", 
                                    font=ctk.CTkFont(size=13, weight="bold"), text_color="#46685b", 
                                    border_color="#46685b", fg_color="#a6b985", hover_color="#213435",
                                    border_width=2, command=self.create_edit_delete_category)
        self.btn_category.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
        
        # ------------------------------
        # SECTION: INFORMATION
        # ------------------------------
        frm_information_categories = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64",
                                                width=400, height=150)
        frm_information_categories.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        
        lbl_title_information = ctk.CTkLabel(frm_information_categories, text="Information", 
                                        fg_color="#46685b", text_color="#e1e3ac", corner_radius=20, 
                                        font=ctk.CTkFont(size=14, weight="bold"))
        lbl_title_information.grid(row=0, column=0, columnspan=2, pady=10)
        
        names_lables = ["Total categories:", "Most used category:", "Predominant type:"]
        
        for i, value in enumerate(names_lables):
            informative_labels = ctk.CTkLabel(frm_information_categories, text=value, 
                                        fg_color="#46685b", text_color="#e1e3ac", corner_radius=20, 
                                        font=ctk.CTkFont(size=13, weight="bold"))
            informative_labels.grid(row=i+1, column=0, padx=5, pady=5)
            
            results_labels = ctk.CTkLabel(frm_information_categories, text="?", 
                                        fg_color="#648a64", text_color="#e1e3ac", corner_radius=20, 
                                        font=ctk.CTkFont(size=13, weight="bold"), wraplength=300)
            results_labels.grid(row=i+1, column=1, padx=5, pady=5)
            self.list_results_labels.append(results_labels)
            
        if not self.parent_ref.empty_table:
            self.information_labels()
        
    def execute_filter(self, event):
        actual_value = self.entry_filter.get()
        option_filter_value = self.option_filter.get()
        column_filter_value = self.column_filter.get()
        dataframe = [tuple(value) for value in self.df.values.tolist()]
        
        if option_filter_value == "==":
            if "," not in actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                index = int(actual_value.strip())-1
                try:
                    df_filtered = self.df.loc[index]
                    values = tuple([value for value in df_filtered.values.tolist()])
                    values = [(int(values[0]), values[1], values[2])]
                    self.refresh(values)
                except Exception:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif "," in actual_value:
                self.entry_filter.configure(border_width=0)
                indexes = [int(index.strip())-1 for index in actual_value.split(",") if index.strip().isdigit()]
                try:
                    df_filtered = self.df.iloc[indexes].drop_duplicates()
                    table_data = [tuple(value) for value in df_filtered.values.tolist()]
                    self.refresh(table_data)
                except Exception:
                    self.entry_filter.configure(border_width=2, border_color="red")
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == ">":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.df[self.df.index > int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == "<":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.df[self.df.index < int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == ">=":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.df[self.df.index >= int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        elif option_filter_value == "<=":
            if actual_value and actual_value.strip().isdigit():
                self.entry_filter.configure(border_width=0)
                df_filtered = self.df[self.df.index <= int(actual_value)-1]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        
        if column_filter_value == "Name":
            if actual_value:
                df_filtered = self.df[self.df["Name"].str.contains(actual_value, case=False)]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            else:
                self.refresh(dataframe)
        
        if column_filter_value == "Category":
            if actual_value == "Expense":
                self.entry_filter.configure(border_width=0)
                df_filtered = self.df[self.df["Category"] == "Expense"]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "Income":
                self.entry_filter.configure(border_width=0)
                df_filtered = self.df[self.df["Category"] == "Income"]
                table_data = [tuple(value) for value in df_filtered.values.tolist()]
                self.refresh(table_data)
            elif actual_value == "":
                self.entry_filter.configure(border_width=0)
                self.refresh(dataframe)
            else:
                self.entry_filter.configure(border_width=2, border_color="red")
        
    def refresh(self, table_data):
        if self.table_categories:
            self.table_categories.destroy()
            self.table_categories = TableCategories(self.frm_table, table_data, parent_ref=self)
            self.table_categories.grid(row=1, column=0, columnspan=3)
        
    def information_labels(self):
        total_data_categories = self.categories
        total_transactions = self.transactions
        total_categories = len(self.categories)
        most_used_category = []
        predominant_type = []
        
        if len(total_transactions) > 0:
            list_categories = {i[4] : 0 for i in total_transactions}
        else:
            list_categories = {"?":0}
            
        if total_categories > 0:
            list_types = {i[2] : 0 for i in total_data_categories}
        else:
            list_types = {"?":0}
        
        for i in total_data_categories:
            list_types[i[2]] += 1
            
        for i in total_transactions:
            list_categories[i[4]] += 1
            
        max_value = max(list_categories.values())
        max_value_predominant_type = max(list_types.values())
            
        for key, value in list_categories.items():
            if value == max_value:
                most_used_category.append(key)
                
        for key, value in list_types.items():
            if value == max_value_predominant_type:
                predominant_type.append(key)
                
        if total_categories > 0:
            self.list_results_labels[0].configure(text=total_categories)
        else:
            self.list_results_labels[0].configure(text="?")
        
        if len(most_used_category) == 1:
            self.list_results_labels[1].configure(text=most_used_category[0])
        elif 2 <= len(most_used_category) <= 3:
            self.list_results_labels[1].configure(text=", ".join(most_used_category))
        elif len(most_used_category) == len(total_transactions):
            self.list_results_labels[1].configure(text="All categories are being used the same number of times")
        else:
            self.list_results_labels[1].configure(text="Many categories are being used the same number of times")
            
        if len(predominant_type) > 1:
            self.list_results_labels[2].configure(text="Same number in both")
        else:
            self.list_results_labels[2].configure(text=predominant_type[0])
        
    def create_edit_delete_category(self):
        actual_state = self.lbl_title.cget("text")
        actual_data_categories = self.categories
        if not self.empty_table:
            actual_data_transactions = [value[4] for value in self.transactions]
        else:
            actual_data_transactions = ""
        new_name = self.entry_name.get()
        new_category = self.smb_category.get()

        if actual_state == "Create":
            for name in actual_data_categories:
                if new_name.strip().lower() == name[1].strip().lower():
                    self.entry_name.delete(0, "end")
                    self.entry_name.configure(border_color="red", border_width=2)
                    self.entry_name.insert(0, "Error: Existing category")
                    self.btn_category.configure(state="disabled")
                    self.after(2000, lambda:self.entry_name.delete(0, "end"))
                    self.after(2000, lambda:self.entry_name.configure(border_width=0))
                    self.after(2000, lambda:self.btn_category.configure(state="normal"))
                    return
            if new_name == "":
                self.entry_name.configure(border_color="red", border_width=2)
                self.entry_name.insert(0, "Error: Enter a name")
                self.btn_category.configure(state="disabled")
                self.after(2000, lambda:self.entry_name.delete(0, "end"))
                self.after(2000, lambda:self.entry_name.configure(border_width=0))
                self.after(2000, lambda:self.btn_category.configure(state="normal"))
                return
            
        if actual_state == "Create":
            self.column_filter.configure(state="normal")
            self.entry_filter.configure(state="normal")
            self.option_filter.configure(state="normal")
            self.dbc.insert_values(Category(new_name, new_category))
            self.load_data()
            self.parent_ref.frm_transaction.cbbox_category.configure(values=self.categories_names)
            self.refresh([tuple(value) for value in self.df.values.tolist()])
            self.information_labels()
            self.refresh_colors()
            self.parent_ref.frm_transaction.colors_cells = self.colors_cells
            self.entry_name.delete(0, "end")
            self.entry_name.focus()
            self.smb_category.set("Income")
        elif actual_state == "Edit":
            self.column_filter.configure(state="normal")
            self.entry_filter.configure(state="normal")
            self.option_filter.configure(state="normal")
            self.dbc.update_values(0, new_name, self.cat_id)
            self.dbc.update_values(1, new_category, self.cat_id)
            self.load_data()
            self.parent_ref.frm_transaction.cbbox_category.configure(values=self.categories_names)
            self.refresh([tuple(value) for value in self.df.values.tolist()])
            self.information_labels()
            self.refresh_colors()
            self.parent_ref.frm_transaction.colors_cells = self.colors_cells
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
                self.column_filter.configure(state="normal")
                self.entry_filter.configure(state="normal")
                self.option_filter.configure(state="normal")
                self.entry_name.configure(state="normal")
                self.smb_category.configure(state="normal")
                self.dbc.delete_values(self.cat_id)
                self.load_data()
                self.parent_ref.frm_transaction.cbbox_category.configure(values=self.categories_names)
                self.refresh([tuple(value) for value in self.df.values.tolist()])
                self.refresh_colors()
                self.parent_ref.frm_transaction.colors_cells = self.colors_cells
                self.information_labels()
                self.lbl_title.configure(text="Create")
                self.entry_name.delete(0, "end")
                self.entry_name.focus()
                self.smb_category.set("Income")
                
    def load_data(self):
        self.categories = self.dbc.check_data(0)
        self.transactions = self.dbt.check_data(0)
        if len(self.categories) > 0:
            self.parent_ref.empty_table = False
            self.df = pd.DataFrame(self.categories, columns=["Index", "Name", "Category"])
            self.df = self.df.reset_index(drop=True)
            self.df["№"] = self.df.index + 1
            self.df = self.df[["№", "Name", "Category"]]
            self.categories_names = [category[1] for category in self.categories]
            self.refresh_colors()
        else:
            self.df = pd.DataFrame(["No data"], columns=["Nothing"])
            self.categories_names = ["Nothing"]
            self.parent_ref.empty_table = True
        self.empty_table = self.parent_ref.empty_table
        
    def refresh_colors(self):
        for category in self.categories:
            if category[2] == "Income":
                self.colors_cells[category[1]] = ("#88B04B", "+")
            else:
                self.colors_cells[category[1]] = ("#BC6C25", "-")