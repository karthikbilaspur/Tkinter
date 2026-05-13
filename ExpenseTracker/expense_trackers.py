import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# =========================
# DATABASE SETUP
# =========================
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")

conn.commit()

# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("750x500")
root.config(bg="#1e1e1e")

# =========================
# STYLES
# =========================
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#2d2d2d",
    foreground="white",
    rowheight=25,
    fieldbackground="#2d2d2d",
)

style.configure(
    "Treeview.Heading",
    background="#444",
    foreground="white",
    font=("Arial", 10, "bold")
)

# =========================
# FUNCTIONS
# =========================

def add_expense():
    title = title_entry.get()
    amount = amount_entry.get()
    category = category_combo.get()
    date = date_entry.get()

    if title == "" or amount == "" or category == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    cursor.execute("""
    INSERT INTO expenses (title, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    conn.commit()

    clear_fields()
    load_expenses()
    update_total()


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)


def delete_expense():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select an expense first!")
        return

    item = tree.item(selected[0])
    expense_id = item["values"][0]

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

    load_expenses()
    update_total()


def clear_fields():
    title_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_combo.set("")
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


def update_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    total_label.config(text=f"Total Expense: ₹{total:.2f}")


# =========================
# INPUT FRAME
# =========================
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

# Title
tk.Label(
    input_frame,
    text="Title",
    bg="#1e1e1e",
    fg="white"
).grid(row=0, column=0, padx=10)

title_entry = tk.Entry(input_frame, width=20)
title_entry.grid(row=0, column=1)

# Amount
tk.Label(
    input_frame,
    text="Amount",
    bg="#1e1e1e",
    fg="white"
).grid(row=0, column=2, padx=10)

amount_entry = tk.Entry(input_frame, width=20)
amount_entry.grid(row=0, column=3)

# Category
tk.Label(
    input_frame,
    text="Category",
    bg="#1e1e1e",
    fg="white"
).grid(row=1, column=0, pady=10)

category_combo = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Other"
    ],
    width=18
)

category_combo.grid(row=1, column=1)

# Date
tk.Label(
    input_frame,
    text="Date",
    bg="#1e1e1e",
    fg="white"
).grid(row=1, column=2)

date_entry = tk.Entry(input_frame, width=20)
date_entry.grid(row=1, column=3)

date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

# =========================
# BUTTONS
# =========================
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

add_btn = tk.Button(
    button_frame,
    text="Add Expense",
    bg="#4CAF50",
    fg="white",
    width=15,
    command=add_expense
)
add_btn.grid(row=0, column=0, padx=10)

delete_btn = tk.Button(
    button_frame,
    text="Delete Expense",
    bg="#f44336",
    fg="white",
    width=15,
    command=delete_expense
)
delete_btn.grid(row=0, column=1, padx=10)

# =========================
# TREEVIEW TABLE
# =========================
columns = ("ID", "Title", "Amount", "Category", "Date")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.pack(pady=10)

# =========================
# TOTAL LABEL
# =========================
total_label = tk.Label(
    root,
    text="Total Expense: ₹0.00",
    font=("Arial", 14, "bold"),
    bg="#1e1e1e",
    fg="#00ff99"
)

total_label.pack(pady=10)

# =========================
# INITIAL LOAD
# =========================
load_expenses()
update_total()

# =========================
# RUN APP
# =========================
root.mainloop()

# =========================
# CLOSE DATABASE
# =========================
conn.close()