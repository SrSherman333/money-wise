import customtkinter as ctk
import tkinter as tk
from src.gui.windows.category_window import CategoryWindow
from src.gui.windows.transaction_window import TransactionWindow
from PIL import Image, ImageTk
from CTkTable import *
import sys, os

def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
            
        return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x650")
        self.title("Money Wise")
        self.configure(fg_color = "#213435")
        self.resizable(False, False)
        
        self.pages = {}
        self.page_name_list = [
            "initial_page",
            "app_page"
        ]
        for name in self.page_name_list:
            frame = ctk.CTkFrame(self, fg_color=("#46685b"), corner_radius=20)
            self.pages[name] = frame
        
        icon_path = resource_path("docs/images/initial_page_logo.png")
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        self.iconphoto(False, icon_image)
        
        self.initial_page()
        self.app_page()
        
    def initial_page(self):
        try:
            logo_image_original = Image.open(resource_path("docs/images/initial_page_logo.png"))
            logo_photo = ctk.CTkImage(dark_image=logo_image_original, size=(150, 150))
        except Exception as e:
            print(e)
            logo_photo = None

        if logo_photo:
            lbl_logo = ctk.CTkLabel(self.pages["initial_page"], text="", bg_color="#46685b", fg_color="#46685b", 
                                    image=logo_photo)
            lbl_logo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        else:
            lbl_logo = ctk.CTkLabel(self.pages["initial_page"], text="😴", bg_color="#46685b", fg_color="#46685b", 
                                    font=ctk.CTkFont(size=64))
            lbl_logo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        lbl_title = ctk.CTkLabel(self.pages["initial_page"], text="MoneyWise", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"),
                                text_color="#e1e3ac", bg_color="#46685b")
        lbl_title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        lbl_subtitle = ctk.CTkLabel(self.pages["initial_page"], text="Your personal financial manager", font=ctk.CTkFont(size=18),
                                    text_color="#e1e3ac", bg_color="#46685b")
        lbl_subtitle.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        btn_start = ctk.CTkButton(self.pages["initial_page"], text="Start", font=ctk.CTkFont(size=20, weight="bold"),
                                text_color="#46685b", bg_color="#46685b", fg_color="#a6b985",
                                hover_color="#213435", command=lambda:self.show_page("app_page"))
        btn_start.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
    def app_page(self):
        tabview = ctk.CTkTabview(self.pages["app_page"], fg_color="#648a64", segmented_button_fg_color="#a6b985",
                        text_color="#46685b", segmented_button_unselected_color="#a6b985",
                        segmented_button_selected_color="#213435", segmented_button_selected_hover_color="#213435",
                        segmented_button_unselected_hover_color="#213435", width=900, height=530)
        tabview.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        tabview.add("Categories")
        tabview.add("Transactions")
        tabview.add("Dashboard")
        tabview.set("Categories")

        actual_tab = tabview.tab("Categories")
        actual_tab.grid_columnconfigure(0, weight=1)
        actual_tab.grid_rowconfigure(1, weight=1)

        for tab_button in tabview._segmented_button._buttons_dict.values():
            tab_button.configure(font=ctk.CTkFont(size=20, weight="bold"))
            
        description = ["This section will display all your existing tags/categories, classified as 'Income' or 'Expense'",
                    "This section will display all existing transactions, and you can filter to search for specific transactions"]
        
        # ------------------------------
        # CATEGORIES TAB
        # ------------------------------
        lbl_subtitle = ctk.CTkLabel(tabview.tab("Categories"), text=description[0], bg_color="#648a64", 
                            fg_color="#a6b985", corner_radius=20, font=ctk.CTkFont(size=15, weight="bold"),
                            text_color="#46685b")
        lbl_subtitle.grid(column=0, row=0, columnspan=2, pady=12)

        self.frm_category = CategoryWindow(tabview.tab("Categories"))
        self.frm_category.grid(column=0, row=1, sticky="nsew", pady=10)
        
        # ------------------------------
        # TRANSACTIONS TAB
        # ------------------------------
        lbl_subtitle = ctk.CTkLabel(tabview.tab("Transactions"), text=description[1], bg_color="#648a64", 
                                    fg_color="#a6b985", corner_radius=20, font=ctk.CTkFont(size=15, weight="bold"),
                                    text_color="#46685b")
        lbl_subtitle.grid(column=0, row=0, pady=12)

        frm_transaction = TransactionWindow(tabview.tab("Transactions"), self)
        frm_transaction.grid(column=0, row=1, sticky="nsew", pady=10)

        btn_back = ctk.CTkButton(self.pages["app_page"], text="Back", font=ctk.CTkFont(size=20, weight="bold"),
                                text_color="#46685b", bg_color="#46685b", fg_color="#a6b985",
                                hover_color="#213435", command=lambda:self.show_page("initial_page"))
        btn_back.place(relx=0.1, rely=0.95, anchor=tk.CENTER)

    def show_page(self, name_page):
        for page in self.pages.values():
            page.pack_forget()
            
        if name_page in self.pages:
            self.pages[name_page].pack(expand=True, fill="both", padx=10, pady=10)
        else:
            print("This page doesn't exists")
    
app = App()
app.show_page("initial_page")
app.mainloop()