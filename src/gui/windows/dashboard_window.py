import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

class DashboardWindow(ctk.CTkFrame):
    def __init__(self, master, parent_ref):
        super().__init__(master)
        self.configure(fg_color = "#648a64")
        self.create_widgets()
        
    def create_widgets(self):
        frm_total_incomes = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=213)
        frm_total_incomes.grid(row=0, column=0, padx=5)
        
        frm_total_expenses = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=213)
        frm_total_expenses.grid(row=0, column=1, padx=5)
        
        frm_current_balance = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=213)
        frm_current_balance.grid(row=0, column=2, padx=5)
        
        frm_percentage_savings = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=213)
        frm_percentage_savings.grid(row=0, column=3, padx=5)
        
        frm_pie_chart = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=434)
        frm_pie_chart.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        
        frm_bar_chart = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=213)
        frm_bar_chart.grid(row=1, column=2, padx=5, pady=10)
        
        frm_line_chart = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=213)
        frm_line_chart.grid(row=1, column=3, padx=5, pady=10)