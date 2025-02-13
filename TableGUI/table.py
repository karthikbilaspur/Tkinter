import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class TableApp:
    def __init__(self, root):
        self.root = root
        self.data = []
        self.headers = []

        self.create_widgets()

    def create_widgets(self):
        # Create table frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill="both", expand=True)

        # Create table headers frame
        self.headers_frame = tk.Frame(self.table_frame)
        self.headers_frame.pack(fill="x")

        # Create table rows frame
        self.rows_frame = tk.Frame(self.table_frame)
        self.rows_frame.pack(fill="both", expand=True)

        # Create buttons frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill="x")

        # Create buttons
        self.add_button = tk.Button(self.buttons_frame, text="Add Row", command=self.add_row)
        self.add_button.pack(side="left")

        self.remove_button = tk.Button(self.buttons_frame, text="Remove Row", command=self.remove_row)
        self.remove_button.pack(side="left")

        self.save_button = tk.Button(self.buttons_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(side="left")

        self.load_button = tk.Button(self.buttons_frame, text="Load Data", command=self.load_data)
        self.load_button.pack(side="left")

    def add_row(self):
        # Create new row
        row = []
        for i in range(len(self.headers)):
            e = tk.Entry(self.rows_frame)
            e.grid(row=len(self.data), column=i)
            row.append(e)
        self.data.append(row)

    def remove_row(self):
        # Remove last row
        if self.data:
            for e in self.data[-1]:
                e.destroy()
            self.data.pop()

    def save_data(self):
        # Get data from entries
        saved_data = []
        for row in self.data:
            saved_row = []
            for e in row:
                saved_row.append(e.get())
            saved_data.append(saved_row)

        # Save data to file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for row in saved_data:
                    f.write(",".join(map(str, row)) + "\n")
            messagebox.showinfo("Data Saved", "Data has been saved successfully.")

    def load_data(self):
        # Load data from file
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.data = []
            for widget in self.rows_frame.winfo_children():
                widget.destroy()
            with open(file_path, "r") as f:
                for i, row in enumerate(f.readlines()):
                    row = row.strip().split(",")
                    row_data = []
                    for j, value in enumerate(row):
                        e = tk.Entry(self.rows_frame)
                        e.grid(row=i, column=j)
                        e.insert(tk.END, value)
                        row_data.append(e)
                    self.data.append(row_data)
            messagebox.showinfo("Data Loaded", "Data has been loaded successfully.")

    def set_headers(self, headers):
        # Set table headers
        self.headers = headers
        for i, header in enumerate(headers):
            e = tk.Entry(self.headers_frame)
            e.grid(row=0, column=i)
            e.insert(tk.END, header)
            e.config(state='readonly')

    def set_data(self, data):
        # Set table data
        self.data = data
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                e = tk.Entry(self.rows_frame)
                e.grid(row=i, column=j)
                e.insert(tk.END, value)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = TableApp(root)

    # Set table headers
    headers = ["ID", "Name", "City", "Age"]
    app.set_headers(headers)

    # Set table data
    data = [
        (1, 'Mohammed', 'Dubai', 19),
        (2, 'Ali', 'Kuala Lumpur', 18),
        (3, 'Fatima', 'Istanbul', 20),
        (4, 'Aisha', 'Cairo', 21),
        (5, 'Omar', 'Riyadh', 21),
        (6, 'Abdullah', 'Jeddah', 22),
        (7, 'Hassan', 'Doha', 20),
        (8, 'Rahman', 'Manama', 21),
        (9, 'Sami', 'Muscat', 19),
        (10, 'Yusuf', 'Abu Dhabi', 22)
    ]
    app.set_data(data)

    root.mainloop()