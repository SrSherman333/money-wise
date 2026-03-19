import customtkinter as ctk
from PIL import Image, ImageTk
from CTkTable import *
from src.core.database import DataBaseCategories
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

class Tables(CTkTable):
    def __init__(self, master, option, total_data_categories, parent_ref, **kwargs):
        self.dbc = DataBaseCategories()
        self.row_clicked = None
        self.state_mode = None
        self.parent_ref = parent_ref
        self.parent = master
        if option == 1:
            data = total_data_categories
            values = [("№", "Name", "Category", "Action")]
            
            for row in data:
                values.append(row + ("",))
        else:
            print("😀")
            
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
