import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class PayrollSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Enterprise Payroll Manager")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f4f7f6")

        self.db_init()
        self.setup_ui()
        self.refresh_employee_list()

    def db_init(self):
        self.conn = sqlite3.connect("payroll.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS employees (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            designation TEXT,
                            gross_salary REAL)""")
        self.conn.commit()

    def setup_ui(self):
        # --- Left: Employee Registration ---
        reg_frame = tk.LabelFrame(self.root, text="Employee Registration", padx=10, pady=10)
        reg_frame.place(x=20, y=20, width=300, height=600)

        fields = [("Name", "name"), ("Designation", "pos"), ("Monthly Gross", "sal")]
        self.entries = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(reg_frame, text=label).pack(anchor="w", pady=5)
            entry = tk.Entry(reg_frame)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry

        tk.Button(reg_frame, text="Add Employee", bg="#27ae60", fg="white", 
                  command=self.add_employee).pack(fill="x", pady=20)

        # --- Middle: Employee Directory ---
        dir_frame = tk.LabelFrame(self.root, text="Employee Directory", padx=10, pady=10)
        dir_frame.place(x=340, y=20, width=320, height=600)

        self.tree = ttk.Treeview(dir_frame, columns=("id", "name", "sal"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("sal", text="Salary")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.generate_slip_data)

        # --- Right: Payslip Preview ---
        slip_frame = tk.LabelFrame(self.root, text="Payslip Generation", padx=10, pady=10)
        slip_frame.place(x=680, y=20, width=300, height=600)

        self.slip_area = tk.Text(slip_frame, font=("Courier", 10), bg="#fff")
        self.slip_area.pack(fill="both", expand=True)
        
        tk.Button(slip_frame, text="Print Payslip", command=lambda: messagebox.showinfo("Print", "Sending to Printer...")).pack(pady=10)

    # --- Core Logic ---

    def add_employee(self):
        name = self.entries['name'].get()
        pos = self.entries['pos'].get()
        sal = self.entries['sal'].get()

        if name and sal:
            self.cur.execute("INSERT INTO employees (name, designation, gross_salary) VALUES (?,?,?)", (name, pos, sal))
            self.conn.commit()
            self.refresh_employee_list()
            messagebox.showinfo("Success", "Employee Added")

    def refresh_employee_list(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT id, name, gross_salary FROM employees")
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)

    def generate_slip_data(self, event):
        selected = self.tree.focus()
        if not selected: return
        
        emp_id = self.tree.item(selected)['values'][0]
        self.cur.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        emp = self.cur.fetchone()

        # Calculations
        gross = emp[3]
        tax = gross * 0.20  # 20% Tax
        insurance = 150.0   # Flat Health Insurance
        net_pay = gross - tax - insurance

        # Payslip Formatting
        slip = f"""
        ==========================
             SALARY PAYSLIP
        ==========================
        ID:      {emp[0]}
        Name:    {emp[1]}
        Role:    {emp[2]}
        Date:    {datetime.now().strftime('%b %Y')}
        --------------------------
        Gross Salary:   ${gross:,.2f}
        
        DEDUCTIONS:
        Tax (20%):      -${tax:,.2f}
        Insurance:      -${insurance:,.2f}
        --------------------------
        NET PAY:        ${net_pay:,.2f}
        ==========================
        """
        self.slip_area.delete("1.0", tk.END)
        self.slip_area.insert(tk.END, slip)

if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollSystem(root)
    root.mainloop()