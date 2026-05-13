import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class HospitalSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("City Hospital Management")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f8f9fa")

        self.db_init()
        self.setup_ui()
        self.refresh_data()

    def db_init(self):
        self.conn = sqlite3.connect("hospital.db")
        self.cur = self.conn.cursor()
        # Patients Table
        self.cur.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, phone TEXT)")
        # Appointments Table
        self.cur.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, p_id INTEGER, doctor TEXT, date TEXT, time TEXT)")
        # Billing Table
        self.cur.execute("CREATE TABLE IF NOT EXISTS billing (id INTEGER PRIMARY KEY, p_id INTEGER, amount REAL, status TEXT)")
        self.conn.commit()

    def setup_ui(self):
        # --- LEFT: Registration & Appointment Entry ---
        input_frame = tk.LabelFrame(self.root, text="Registration & Scheduling", padx=10, pady=10)
        input_frame.place(x=20, y=20, width=350, height=650)

        # Patient Section
        tk.Label(input_frame, text="Patient Name:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.p_name = tk.Entry(input_frame, width=40)
        self.p_name.pack(pady=5)

        tk.Label(input_frame, text="Age:").pack(anchor="w")
        self.p_age = tk.Entry(input_frame, width=10)
        self.p_age.pack(pady=5, anchor="w")

        tk.Button(input_frame, text="Register Patient", command=self.add_patient, bg="#007bff", fg="white").pack(pady=10, fill="x")

        tk.Canvas(input_frame, height=2, bg="#ddd", highlightthickness=0).pack(fill="x", pady=20)

        # Appointment Section
        tk.Label(input_frame, text="Doctor Name:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.doc_name = ttk.Combobox(input_frame, values=["Dr. Smith (GP)", "Dr. Jones (Cardio)", "Dr. Lee (Neuro)"])
        self.doc_name.pack(pady=5, fill="x")

        tk.Label(input_frame, text="Date (YYYY-MM-DD):").pack(anchor="w")
        self.app_date = tk.Entry(input_frame)
        self.app_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.app_date.pack(pady=5, fill="x")

        tk.Button(input_frame, text="Schedule Appointment", command=self.add_appointment, bg="#28a745", fg="white").pack(pady=10, fill="x")

        # --- RIGHT: Tabs for Records ---
        self.tabs = ttk.Notebook(self.root)
        self.tabs.place(x=390, y=20, width=680, height=650)

        # Tab 1: Patient List
        self.p_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.p_tab, text="Patient Directory")
        self.p_tree = ttk.Treeview(self.p_tab, columns=("id", "name", "age", "phone"), show="headings")
        self.p_tree.heading("id", text="ID"); self.p_tree.heading("name", text="Name")
        self.p_tree.pack(fill="both", expand=True)

        # Tab 2: Appointment Calendar
        self.a_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.a_tab, text="Appointments")
        self.a_tree = ttk.Treeview(self.a_tab, columns=("id", "p_id", "doc", "date", "time"), show="headings")
        self.a_tree.heading("id", text="Appt ID"); self.a_tree.heading("p_id", text="Patient ID")
        self.a_tree.pack(fill="both", expand=True)

        # Tab 3: Billing
        self.b_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.b_tab, text="Billing Dept")
        self.b_tree = ttk.Treeview(self.b_tab, columns=("id", "p_id", "amt", "status"), show="headings")
        self.b_tree.heading("amt", text="Amount"); self.b_tree.heading("status", text="Status")
        self.b_tree.pack(fill="both", expand=True)
        
        tk.Button(self.b_tab, text="Generate Bill ($150)", command=self.create_bill).pack(pady=5)

    # --- Logic Operations ---

    def add_patient(self):
        name = self.p_name.get()
        if name:
            self.cur.execute("INSERT INTO patients (name, age) VALUES (?,?)", (name, self.p_age.get()))
            self.conn.commit()
            self.refresh_data()
            messagebox.showinfo("Success", f"Patient {name} registered.")

    def add_appointment(self):
        selected = self.p_tree.focus()
        if not selected:
            messagebox.showwarning("Selection", "Select a patient from the Directory first!")
            return
        
        p_id = self.p_tree.item(selected)['values'][0]
        self.cur.execute("INSERT INTO appointments (p_id, doctor, date) VALUES (?,?,?)", 
                         (p_id, self.doc_name.get(), self.app_date.get()))
        self.conn.commit()
        self.refresh_data()

    def create_bill(self):
        selected = self.p_tree.focus()
        if not selected: return
        p_id = self.p_tree.item(selected)['values'][0]
        self.cur.execute("INSERT INTO billing (p_id, amount, status) VALUES (?,?,?)", (p_id, 150.0, "Unpaid"))
        self.conn.commit()
        self.refresh_data()

    def refresh_data(self):
        # Clear and reload all trees
        for tree, table in [(self.p_tree, "patients"), (self.a_tree, "appointments"), (self.b_tree, "billing")]:
            tree.delete(*tree.get_children())
            self.cur.execute(f"SELECT * FROM {table}")
            for row in self.cur.fetchall(): tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalSystem(root)
    root.mainloop()