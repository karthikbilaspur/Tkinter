import tkinter as tk
from tkinter import messagebox

class PercentileCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Percentile Calculator")

        # Create entry fields
        tk.Label(self.window, text="Rank").grid(row=0, column=0)
        self.rank_field = tk.Entry(self.window, width=20)
        self.rank_field.grid(row=0, column=1)

        tk.Label(self.window, text="Total Participants").grid(row=1, column=0)
        self.total_participants_field = tk.Entry(self.window, width=20)
        self.total_participants_field.grid(row=1, column=1)

        # Create buttons
        tk.Button(self.window, text="Calculate Percentile", command=self.calculate_percentile).grid(row=2, column=0)
        tk.Button(self.window, text="Clear", command=self.clear_fields).grid(row=2, column=1)
        tk.Button(self.window, text="Exit", command=self.window.destroy).grid(row=2, column=2)

        # Create result field
        tk.Label(self.window, text="Percentile").grid(row=3, column=0)
        self.percentile_field = tk.Entry(self.window, width=20)
        self.percentile_field.grid(row=3, column=1)

        # Create status bar
        self.status_bar = tk.Label(self.window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, columnspan=3)

        # Create menu bar
        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar)
        self.file_menu.add_command(label="Exit", command=self.window.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = tk.Menu(self.menu_bar)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def calculate_percentile(self):
        try:
            rank = int(self.rank_field.get())
            total_participants = int(self.total_participants_field.get())

            if rank < 1 or total_participants < 1:
                raise ValueError("Rank and total participants must be positive integers.")

            if rank > total_participants:
                raise ValueError("Rank cannot be greater than total participants.")

            percentile = round((total_participants - rank) / total_participants * 100, 3)
            self.percentile_field.delete(0, tk.END)
            self.percentile_field.insert(0, str(percentile))
            self.status_bar.config(text="Calculation successful!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.status_bar.config(text="Error occurred!")

    def clear_fields(self):
        self.rank_field.delete(0, tk.END)
        self.total_participants_field.delete(0, tk.END)
        self.percentile_field.delete(0, tk.END)
        self.status_bar.config(text="Ready")

    def show_about(self):
        messagebox.showinfo("About", "Percentile Calculator v1.0")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = PercentileCalculator()
    calculator.run()