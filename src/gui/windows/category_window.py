import customtkinter as ctk
import tkinter as tk
from src.gui.components.tables import Tables
from src.core.database import DataBaseCategories, DataBaseTransactions
from src.core.models import Category

class CategoryWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.dbc = DataBaseCategories()
        self.dbt = DataBaseTransactions()
        self.cat_id = None
        self.list_results_labels = []
        self.configure(fg_color = "#648a64")
        self.create_widgets()
        
    def create_widgets(self):
        # ------------------------------
        # SECTION: TABLE
        # ------------------------------
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        frm_table = ctk.CTkScrollableFrame(self, fg_color="#a6b985", bg_color="#648a64", width=450,
                                        scrollbar_button_color="#46685b", scrollbar_button_hover_color="#213435")
        frm_table.grid(row=0, column=0, sticky="nsew", rowspan=2, padx=5)
        
        lbl_title_table = ctk.CTkLabel(frm_table, text="Table of Categories", 
                            fg_color="#46685b", text_color="#e1e3ac", corner_radius=20, 
                            font=ctk.CTkFont(size=14, weight="bold"))
        lbl_title_table.grid(row=0, column=0, pady=10)
        
        total_data_categories = self.dbc.check_data(0)
        self.table_categories = Tables(frm_table, 1, total_data_categories, parent_ref=self)
        self.table_categories.grid(row=1, column=0)
            
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
            
        self.information_labels(total_data_categories)
        
    def information_labels(self, total_data_categories):
        total_transactions = self.dbt.check_data(0)
        total_categories = len(total_data_categories)
        most_used_category = []
        predominant_type = []
        
        list_categories = {i[4] : 0 for i in total_transactions}
        list_types = {i[2] : 0 for i in total_data_categories}
        
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
                
        self.list_results_labels[0].configure(text=total_categories)
        
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
                self.table_categories.refresh()
                self.information_labels(self.dbc.check_data(0))
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
                self.table_categories.refresh()
                self.information_labels(self.dbc.check_data(0))
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
                self.dbc.delete_values(self.cat_id)
                self.table_categories.refresh()
                self.information_labels(self.dbc.check_data(0))
                self.lbl_title.configure(text="Create")
                self.entry_name.delete(0, "end")
                self.entry_name.focus()
                self.smb_category.set("Income")
                self.entry_name.configure(state="disabled")