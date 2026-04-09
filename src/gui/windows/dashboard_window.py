from tkinter import font
import customtkinter as ctk
from pandas.io.formats.printing import _justify
from src.core.analyzer import Analyzer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class DashboardWindow(ctk.CTkFrame):
    def __init__(self, master, parent_ref):
        super().__init__(master)
        self.configure(fg_color = "#648a64")
        self.analyzer = parent_ref.frm_transaction.analyzer
        self.create_widgets()
        
    def create_widgets(self):
        # Total incomes chart
        frm_total_incomes = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=293, height=180)
        frm_total_incomes.grid(row=0, column=0, padx=5)

        lbl_title = ctk.CTkLabel(frm_total_incomes, text="Total Incomes", text_color="#213435", font=ctk.CTkFont(size=12))
        lbl_title.place(relx=0.05, rely=0.05)

        total_incomes = f"+{self.analyzer.total_incomes:.2f}$"
        lbl_value = ctk.CTkLabel(frm_total_incomes, text=total_incomes, text_color="#213435", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_value.place(relx=0.05, rely=0.15)

        fig = self.analyzer.total_incomes_chart()
        canvas = FigureCanvasTkAgg(fig, master=frm_total_incomes)
        canvas.get_tk_widget().config(bd=0, highlightthickness=0)
        canvas.get_tk_widget().config(bg="#a6b985")
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.4, rely=0.01)
        
        # Total expenses chart
        frm_total_expenses = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=293, height=180)
        frm_total_expenses.grid(row=0, column=1, padx=5)

        lbl_title = ctk.CTkLabel(frm_total_expenses, text="Total Expenses", text_color="#213435", font=ctk.CTkFont(size=12))
        lbl_title.place(relx=0.05, rely=0.05)

        total_expenses = f"-{self.analyzer.total_expenses:.2f}$"
        lbl_value = ctk.CTkLabel(frm_total_expenses, text=total_expenses, text_color="#213435", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_value.place(relx=0.05, rely=0.15)

        fig = self.analyzer.total_expenses_chart()
        canvas = FigureCanvasTkAgg(fig, master=frm_total_expenses)
        canvas.get_tk_widget().config(bd=0, highlightthickness=0)
        canvas.get_tk_widget().config(bg="#a6b985")
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.4, rely=0.01)
        
        # Percentage Savings chart
        frm_percentage_savings = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=293, height=180)
        frm_percentage_savings.grid(row=0, column=2, padx=5)
        
        lbl_title = ctk.CTkLabel(frm_percentage_savings, text=f"Percentage\nSavings", text_color="#213435", 
            font=ctk.CTkFont(size=12), justify="left")
        lbl_title.place(relx=0.05, rely=0.05)

        current_balance = f"{self.analyzer.current_balance:.2f}$"
        lbl_value = ctk.CTkLabel(frm_percentage_savings, text=current_balance, text_color="#213435", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_value.place(relx=0.05, rely=0.2)

        fig = self.analyzer.percentage_saving_chart()
        canvas = FigureCanvasTkAgg(fig, master=frm_percentage_savings)
        canvas.get_tk_widget().config(bd=0, highlightthickness=0)
        canvas.get_tk_widget().config(bg="#a6b985")
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.4, rely=0.01)

        # Pie chart
        frm_pie_chart = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=293, height=265)
        frm_pie_chart.grid(row=1, column=0, padx=5, pady=(10,0))
        
        lbl_title = ctk.CTkLabel(frm_pie_chart, text="Distribution of Expenses", text_color="#213435", 
        font=ctk.CTkFont(size=12), justify="left")
        lbl_title.place(relx=0.05, rely=0.05)

        fig = self.analyzer.pie_chart()
        canvas = FigureCanvasTkAgg(fig, master=frm_pie_chart)
        canvas.get_tk_widget().config(bd=0, highlightthickness=0)
        canvas.get_tk_widget().config(bg="#a6b985")
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.01, rely=0.15)
        
        # Line chart
        frm_line_chart = ctk.CTkFrame(self, fg_color="#a6b985", bg_color="#648a64", width=594, height=265)
        frm_line_chart.grid(row=1, column=1, columnspan=2, padx=5, pady=(10,0))

        lbl_title = ctk.CTkLabel(frm_line_chart, text="Evolution of Transactions", text_color="#213435", 
        font=ctk.CTkFont(size=12), justify="left")
        lbl_title.place(relx=0.05, rely=0.05)

        fig = self.analyzer.line_chart()
        canvas = FigureCanvasTkAgg(fig, master=frm_line_chart)
        canvas.get_tk_widget().config(bd=0, highlightthickness=0)
        canvas.get_tk_widget().config(bg="#a6b985")
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.00, rely=0.12)