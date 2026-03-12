import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from CTkTable import *

app = ctk.CTk()
app.geometry("500x450")
app.title("Money Wise")
app.configure(fg_color = "#213435")
app.resizable(False, False)

pages = {}

def show_page(name_page):
    for page in pages.values():
        page.place_forget()
        
    if name_page in pages:
        pages[name_page].pack(expand=True, fill="both", padx=10, pady=10)
    else:
        print("This page doesn't exists")
        
page_name_list = [
    "initial_page",
    "app_page"
]

for name in page_name_list:
    frame = ctk.CTkFrame(app, fg_color=("#46685b"), corner_radius=20)
    pages[name] = frame
    
# INITIAL PAGE INTERFACE --------------------------------------------------------------------------------
try:
    logo_image_original = Image.open("docs/images/initial_page_logo.png")
    logo_photo = ctk.CTkImage(dark_image=logo_image_original, size=(150, 150))
except Exception as e:
    print(e)
    logo_photo = None

if logo_photo:
    lbl_logo = ctk.CTkLabel(app, text="", bg_color="#46685b", fg_color="#46685b", image=logo_photo)
    lbl_logo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
else:
    lbl_logo = ctk.CTkLabel(app, text="😴", bg_color="#46685b", fg_color="#46685b", font=ctk.CTkFont(size=64))
    lbl_logo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

lbl_title = ctk.CTkLabel(app, text="MoneyWise", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"),
                        text_color="#e1e3ac", bg_color="#46685b")
lbl_title.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

lbl_subtitle = ctk.CTkLabel(app, text="Your personal financial manager", font=ctk.CTkFont(size=18),
                            text_color="#e1e3ac", bg_color="#46685b")
lbl_subtitle.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

btn_start = ctk.CTkButton(app, text="Start", font=ctk.CTkFont(size=20, weight="bold"),
                        text_color="#46685b", bg_color="#46685b", fg_color="#a6b985",
                        hover_color="#213435")
btn_start.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

show_page("initial_page")
app.mainloop()