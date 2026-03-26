import customtkinter as ctk
import pandas as pd
from PIL import Image, ImageTk
from CTkTable import *
from src.core.database import DataBaseCategories, DataBaseTransactions
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

class TableCategories(CTkTable):
    def __init__(self, master, total_data_categories, parent_ref, **kwargs):
        self.dbc = DataBaseCategories()
        self.row_clicked = None
        self.state_mode = None
        self.parent_ref = parent_ref
        self.parent = master
        data = total_data_categories
        values = [("№", "Name", "Category", "Action")]
        
        for row in data:
            values.append(row + ("",))
            
        weights = [40, 200, 120, 50]
        super().__init__(master, values=values, **kwargs)
        
        for i, row in enumerate(data, start=1):
            self.insert(i, column=0, value=i)
        
        for i, weight in enumerate(weights):
            self.edit_column(i, width=weight)
            
        self.configure(bg_color="#a6b985", text_color="#e1e3ac", header_color="#213435", 
                    colors=["#46685b", "#648a64"])
        
        for col in range(4):
            value = self.get(0, col)
            self.insert(row=0, column=col, value=value, corner_radius=15, font=ctk.CTkFont(size=13, weight="bold"))
            
        try:
            trash_icon_original = Image.open(resource_path("docs/images/trash_icon.png"))
            trash_icon_photo = ctk.CTkImage(light_image=trash_icon_original, size=(16, 16))
        except Exception as e:
            print(e)
            trash_icon_photo = None
        
        for i, row in enumerate(data, start=1):
            category_id = row[0]
            actual_row = i
            
            self.insert(
                row=i, column=3, value="", image=trash_icon_photo,
                command=lambda id_cat = category_id, act_row = actual_row: self.select_category(id_cat, act_row, "delete")
            )
            self.edit(row=i, column=3, hover=True, hover_color="red")
            self.edit(row=i, column=1, hover=True, hover_color="#213435", 
                    command=lambda id_cat = category_id, act_row = actual_row: self.select_category(id_cat, act_row, "edit"))
        
    def select_category(self, id_cat, act_row, option):
        self.parent_ref.cat_id = id_cat
        
        if option == "edit":
            self.parent_ref.lbl_title.configure(text="Edit")
            
            if self.row_clicked is not None and self.row_clicked != act_row:
                self.edit_row(self.row_clicked, border_width=0)
                self.parent_ref.entry_name.configure(state="normal")
                self.parent_ref.smb_category.configure(state="normal")
                
            if self.row_clicked == act_row and option == self.state_mode:
                self.edit_row(self.row_clicked, border_width=0)
                self.row_clicked = None
                self.parent_ref.entry_name.configure(state="normal")
                self.parent_ref.smb_category.configure(state="normal")
                self.parent_ref.entry_name.delete(0, "end")
                self.parent_ref.entry_name.focus()
                self.parent_ref.lbl_title.configure(text="Create")
                self.parent_ref.smb_category.set("Income")
            elif self.row_clicked == act_row and option != self.state_mode:
                self.edit_row(act_row, border_width=2, border_color="white")
                self.state_mode = "edit"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.entry_name.configure(state="normal")
                self.parent_ref.smb_category.configure(state="normal")
                self.parent_ref.entry_name.delete(0, "end")
                self.parent_ref.entry_name.insert(0, values_act_row[1])
                self.parent_ref.smb_category.set(values_act_row[2])
                self.parent_ref.entry_name.focus()
            else:
                self.edit_row(act_row, border_width=2, border_color="white")
                self.state_mode = "edit"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.entry_name.configure(state="normal")
                self.parent_ref.smb_category.configure(state="normal")
                self.parent_ref.entry_name.delete(0, "end")
                self.parent_ref.entry_name.insert(0, values_act_row[1])
                self.parent_ref.smb_category.set(values_act_row[2])
                self.parent_ref.entry_name.focus()
        else:
            self.parent_ref.lbl_title.configure(text="Delete")
            if self.row_clicked is not None and self.row_clicked != act_row:
                self.edit_row(self.row_clicked, border_width=0)
                self.parent_ref.entry_name.configure(state="normal")
                self.parent_ref.smb_category.configure(state="normal")
                
            if self.row_clicked == act_row and option == self.state_mode:
                self.edit_row(self.row_clicked, border_width=0)
                self.row_clicked = None
                self.parent_ref.entry_name.configure(state="normal")
                self.parent_ref.smb_category.configure(state="normal")
                self.parent_ref.entry_name.delete(0, "end")
                self.parent_ref.entry_name.focus()
                self.parent_ref.lbl_title.configure(text="Create")
                self.parent_ref.smb_category.set("Income")
            elif self.row_clicked == act_row and option != self.state_mode:
                self.edit_row(act_row, border_width=2, border_color="red")
                self.state_mode = "delete"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.entry_name.delete(0, "end")
                self.parent_ref.entry_name.insert(0, values_act_row[1])
                self.parent_ref.entry_name.configure(state="disabled")
                self.parent_ref.smb_category.configure(state="disabled")
                self.parent_ref.smb_category.set(values_act_row[2])
                self.parent_ref.entry_name.focus()
            else:
                self.edit_row(act_row, border_width=2, border_color="red")
                self.state_mode = "delete"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.entry_name.delete(0, "end")
                self.parent_ref.entry_name.insert(0, values_act_row[1])
                self.parent_ref.entry_name.configure(state="disabled")
                self.parent_ref.smb_category.configure(state="disabled")
                self.parent_ref.smb_category.set(values_act_row[2])
                self.parent_ref.entry_name.focus()
                
                
class TableTransactions(CTkTable):
    def __init__(self, master, total_data_transactions, parent_ref, **kwargs):
        self.dbt = DataBaseTransactions()
        self.row_clicked = None
        self.state_mode = None
        self.parent_ref = parent_ref
        self.parent = master
        data = total_data_transactions
        values = [("№", "Date", "Concept", "Amount", "Category", "Action")]
        
        for row in data:
            values.append(row + ("",))
            
        weights = [40, 100, 405, 100, 120, 50]
        super().__init__(master, values=values, **kwargs)
        
        for i, weight in enumerate(weights):
            self.edit_column(i, width=weight)
            
        self.configure(bg_color="#a6b985", text_color="#e1e3ac", header_color="#213435", 
                    colors=["#46685b", "#648a64"])
        
        for col in range(6):
            value = self.get(0, col)
            self.insert(row=0, column=col, value=value, corner_radius=15, font=ctk.CTkFont(size=13, weight="bold"))
            
        try:
            trash_icon_original = Image.open(resource_path("docs/images/trash_icon.png"))
            trash_icon_photo = ctk.CTkImage(light_image=trash_icon_original, size=(16, 16))
        except Exception as e:
            print(e)
            trash_icon_photo = None
        
        for i, row in enumerate(data, start=1):
            category_id = row[0]
            actual_row = i
            category = self.get(i, column=4)
            
            amount = str(self.get(i, column=3))

            if "-" in amount:
                amount = amount.replace("-", "")
                amount = amount.replace("$", "")
            elif "+" in amount:
                amount = amount.replace("+", "")
                amount = amount.replace("$", "")
            else:
                pass
            
            self.insert(
                row=i, column=5, value="", image=trash_icon_photo,
                command=lambda id_cat = category_id, act_row = actual_row: self.select_category(id_cat, act_row, "delete")
            )
            self.edit(row=i, column=5, hover=True, hover_color="red")
            self.edit(row=i, column=2, hover=True, hover_color="#213435", 
                    command=lambda id_cat = category_id, act_row = actual_row: self.select_category(id_cat, act_row, "edit"))
            self.edit(row=i, column=3, fg_color=parent_ref.colors_cells[category][0], text=parent_ref.colors_cells[category][1]+amount+"$")
        
    def select_category(self, id_cat, act_row, option):
        self.parent_ref.cat_id = id_cat
        
        if option == "edit":
            self.parent_ref.lbl_title.configure(text="Edit")
            
            if self.row_clicked is not None and self.row_clicked != act_row:
                self.edit_row(self.row_clicked, border_width=0)
                self.parent_ref.calendar.date_entry.configure(state="normal")
                self.parent_ref.txtbox_concept.configure(state="normal")
                self.parent_ref.entry_amount.configure(state="normal")
                self.parent_ref.cbbox_category.configure(state="normal")
                self.parent_ref.column_filter.configure(state="normal")
                self.parent_ref.entry_filter.configure(state="normal")
                self.parent_ref.option_filter.configure(state="normal")
                
            if self.row_clicked == act_row and option == self.state_mode:
                self.edit_row(self.row_clicked, border_width=0)
                self.row_clicked = None
                self.parent_ref.calendar.date_entry.configure(state="normal")
                self.parent_ref.txtbox_concept.configure(state="normal")
                self.parent_ref.entry_amount.configure(state="normal")
                self.parent_ref.cbbox_category.configure(state="normal")
                self.parent_ref.column_filter.configure(state="normal")
                self.parent_ref.entry_filter.configure(state="normal")
                self.parent_ref.option_filter.configure(state="normal")
                self.parent_ref.calendar.date_entry.delete(0, "end")
                self.parent_ref.calendar.date_entry.focus()
                self.parent_ref.txtbox_concept.delete("1.0", "end")
                self.parent_ref.entry_amount.delete(0, "end")
                self.parent_ref.cbbox_category.set(self.parent_ref.categories_names[0])
                self.parent_ref.entry_amount.configure(border_width=2, border_color=self.parent_ref.colors_cells[self.parent_ref.categories_names[0]][0])
                self.parent_ref.lbl_title.configure(text="Create")
            elif self.row_clicked == act_row and option != self.state_mode:
                self.edit_row(act_row, border_width=2, border_color="white")
                self.state_mode = "edit"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.calendar.date_entry.configure(state="normal")
                self.parent_ref.txtbox_concept.configure(state="normal")
                self.parent_ref.entry_amount.configure(state="normal")
                self.parent_ref.cbbox_category.configure(state="normal")
                self.parent_ref.column_filter.configure(state="disabled")
                self.parent_ref.entry_filter.configure(state="disabled")
                self.parent_ref.option_filter.configure(state="disabled")
                self.parent_ref.calendar.date_entry.delete(0, "end")
                self.parent_ref.calendar.date_entry.insert(0, values_act_row[1])
                self.parent_ref.txtbox_concept.delete("1.0", "end")
                self.parent_ref.txtbox_concept.insert("0.0", values_act_row[2])
                self.parent_ref.entry_amount.delete(0, "end")
                values_act_row[3] = values_act_row[3].replace("$", "")
                if "+" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("+", "")
                elif "-" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("-", "")
                self.parent_ref.entry_amount.insert(0, values_act_row[3])
                self.parent_ref.cbbox_category.set(values_act_row[4])
                self.parent_ref.entry_amount.configure(border_width=2, border_color=self.parent_ref.colors_cells[values_act_row[4]][0])
                self.parent_ref.calendar.date_entry.focus()
            else:
                self.edit_row(act_row, border_width=2, border_color="white")
                self.state_mode = "edit"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.calendar.date_entry.configure(state="normal")
                self.parent_ref.txtbox_concept.configure(state="normal")
                self.parent_ref.entry_amount.configure(state="normal")
                self.parent_ref.cbbox_category.configure(state="normal")
                self.parent_ref.column_filter.configure(state="disabled")
                self.parent_ref.entry_filter.configure(state="disabled")
                self.parent_ref.option_filter.configure(state="disabled")
                self.parent_ref.calendar.date_entry.delete(0, "end")
                self.parent_ref.calendar.date_entry.insert(0, values_act_row[1])
                self.parent_ref.txtbox_concept.delete("1.0", "end")
                self.parent_ref.txtbox_concept.insert("0.0", values_act_row[2])
                values_act_row[3] = values_act_row[3].replace("$", "")
                if "+" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("+", "")
                elif "-" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("-", "")
                self.parent_ref.entry_amount.delete(0, "end")
                self.parent_ref.entry_amount.insert(0, values_act_row[3])
                self.parent_ref.cbbox_category.set(values_act_row[4])
                self.parent_ref.entry_amount.configure(border_width=2, border_color=self.parent_ref.colors_cells[values_act_row[4]][0])
                self.parent_ref.calendar.date_entry.focus()
        else:
            self.parent_ref.lbl_title.configure(text="Delete")
            
            if self.row_clicked is not None and self.row_clicked != act_row:
                self.edit_row(self.row_clicked, border_width=0)
                self.parent_ref.calendar.date_entry.configure(state="normal")
                self.parent_ref.txtbox_concept.configure(state="normal")
                self.parent_ref.entry_amount.configure(state="normal")
                self.parent_ref.cbbox_category.configure(state="normal")
                self.parent_ref.column_filter.configure(state="normal")
                self.parent_ref.entry_filter.configure(state="normal")
                self.parent_ref.option_filter.configure(state="normal")
                
            if self.row_clicked == act_row and option == self.state_mode:
                self.edit_row(self.row_clicked, border_width=0)
                self.row_clicked = None
                self.parent_ref.calendar.date_entry.configure(state="normal")
                self.parent_ref.txtbox_concept.configure(state="normal")
                self.parent_ref.entry_amount.configure(state="normal")
                self.parent_ref.cbbox_category.configure(state="normal")
                self.parent_ref.column_filter.configure(state="normal")
                self.parent_ref.entry_filter.configure(state="normal")
                self.parent_ref.option_filter.configure(state="normal")
                self.parent_ref.calendar.date_entry.delete(0, "end")
                self.parent_ref.calendar.date_entry.focus()
                self.parent_ref.txtbox_concept.delete("1.0", "end")
                self.parent_ref.entry_amount.delete(0, "end")
                self.parent_ref.cbbox_category.set(self.parent_ref.categories_names[0])
                self.parent_ref.entry_amount.configure(border_width=2, border_color=self.parent_ref.colors_cells[self.parent_ref.categories_names[0]][0])
                self.parent_ref.lbl_title.configure(text="Create")
            elif self.row_clicked == act_row and option != self.state_mode:
                self.edit_row(act_row, border_width=2, border_color="red")
                self.state_mode = "delete"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.calendar.date_entry.delete(0, "end")
                self.parent_ref.calendar.date_entry.insert(0, values_act_row[1])
                self.parent_ref.calendar.date_entry.configure(state="disabled")
                self.parent_ref.txtbox_concept.delete("1.0", "end")
                self.parent_ref.txtbox_concept.insert("0.0", values_act_row[2])
                self.parent_ref.txtbox_concept.configure(state="disabled")
                values_act_row[3] = values_act_row[3].replace("$", "")
                if "+" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("+", "")
                elif "-" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("-", "")
                self.parent_ref.entry_amount.delete(0, "end")
                self.parent_ref.entry_amount.insert(0, values_act_row[3])
                self.parent_ref.cbbox_category.set(values_act_row[4])
                self.parent_ref.entry_amount.configure(border_width=2, border_color=self.parent_ref.colors_cells[values_act_row[4]][0])
                self.parent_ref.entry_amount.configure(state="disabled")
                self.parent_ref.cbbox_category.configure(state="disabled")
                self.parent_ref.column_filter.configure(state="disabled")
                self.parent_ref.entry_filter.configure(state="disabled")
                self.parent_ref.option_filter.configure(state="disabled")
            else:
                self.edit_row(act_row, border_width=2, border_color="red")
                self.state_mode = "delete"
                self.row_clicked = act_row
                values_act_row = self.get_row(act_row)
                self.parent_ref.calendar.date_entry.delete(0, "end")
                self.parent_ref.calendar.date_entry.insert(0, values_act_row[1])
                self.parent_ref.calendar.date_entry.configure(state="disabled")
                self.parent_ref.txtbox_concept.delete("1.0", "end")
                self.parent_ref.txtbox_concept.insert("0.0", values_act_row[2])
                self.parent_ref.txtbox_concept.configure(state="disabled")
                values_act_row[3] = values_act_row[3].replace("$", "")
                if "+" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("+", "")
                elif "-" in values_act_row[3]:
                    values_act_row[3] = values_act_row[3].replace("-", "")
                self.parent_ref.entry_amount.delete(0, "end")
                self.parent_ref.entry_amount.insert(0, values_act_row[3])
                self.parent_ref.cbbox_category.set(values_act_row[4])
                self.parent_ref.entry_amount.configure(border_width=2, border_color=self.parent_ref.colors_cells[values_act_row[4]][0])
                self.parent_ref.entry_amount.configure(state="disabled")
                self.parent_ref.cbbox_category.configure(state="disabled")
                self.parent_ref.column_filter.configure(state="disabled")
                self.parent_ref.entry_filter.configure(state="disabled")
                self.parent_ref.option_filter.configure(state="disabled")
