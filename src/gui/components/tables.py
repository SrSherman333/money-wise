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
            
            self.insert(
                row=i, column=3, value="", image=trash_icon_photo,
                command=lambda id_cat = category_id: self.delete_category(id_cat)
            )
            self.edit(row=i, column=3, hover=True, hover_color="red")
            self.edit(row=i, column=1, hover=True, hover_color="#213435", 
                    command=lambda id_cat = category_id: self.edit_category(id_cat))
            
    def delete_category(self, id_cat):
        self.dbc.delete_values(id_cat)
        self.refresh()
        self.parent_ref.information_labels(self.dbc.check_data(0))
        
    def refresh(self):
        self.destroy()
        lbl_title_table = ctk.CTkLabel(self.parent, text="Table of Categories", 
                            fg_color="#46685b", text_color="#e1e3ac", corner_radius=20, 
                            font=ctk.CTkFont(size=14, weight="bold"))
        lbl_title_table.grid(row=0, column=0, pady=10)
        table_categories = Tables(self.parent, 1, self.dbc.check_data(0), self.parent_ref)
        table_categories.grid(row=1, column=0)
        
    def edit_category(self, id_cat):
        print(id_cat)