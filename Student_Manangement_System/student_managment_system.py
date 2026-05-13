import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")
        
        self.db_init()
        self.setup_ui()
        self.display_students()

    def db_init(self):
        """Initialize the SQLite database."""
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                attendance TEXT
            )
        """)
        self.conn.commit()

    def setup_ui(self):
        # --- Left Input Frame ---
        input_frame = tk.LabelFrame(self.root, text="Manage Student", font=("Arial", 12, "bold"), padx=10, pady=10)
        input_frame.place(x=20, y=20, width=350, height=550)

        labels = ["ID", "Name", "Email", "Gender", "Contact", "Attendance"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label).grid(row=i, column=0, pady=10, sticky="w")
            if label == "Gender":
                entry = ttk.Combobox(input_frame, values=["Male", "Female", "Other"], state="readonly")
            elif label == "Attendance":
                entry = ttk.Combobox(input_frame, values=["Present", "Absent"], state="readonly")
            else:
                entry = tk.Entry(input_frame)
            
            entry.grid(row=i, column=1, pady=10, padx=10)
            self.entries[label.lower()] = entry

        # Buttons
        btn_frame = tk.Frame(input_frame)
        btn_frame.grid(row=len(labels), columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Add", command=self.add_student, width=8, bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_student, width=8, bg="blue", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_student, width=8, bg="red", fg="white").pack(side="left", padx=5)

        # --- Right Display Frame ---
        display_frame = tk.Frame(self.root, bd=2, relief="ridge")
        display_frame.place(x=390, y=20, width=580, height=550)

        # Search Bar
        search_frame = tk.Frame(display_frame)
        search_frame.pack(side="top", fill="x", pady=10)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=10, expand=True, fill="x")
        tk.Button(search_frame, text="Search", command=self.search_students).pack(side="right", padx=10)

        # Treeview (Table)
        self.tree = ttk.Treeview(display_frame, columns=("id", "name", "email", "gender", "contact", "attendance"), show="headings")
        for col in ("id", "name", "email", "gender", "contact", "attendance"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=90)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.get_cursor)

    # --- Logic ---

    def add_student(self):
        data = [self.entries[k].get() for k in ["id", "name", "email", "gender", "contact", "attendance"]]
        if "" in data:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            self.cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?)", data)
            self.conn.commit()
            self.display_students()
            self.clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "ID already exists!")

    def display_students(self, rows=None):
        self.tree.delete(*self.tree.get_children())
        if rows is None:
            self.cursor.execute("SELECT * FROM students")
            rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def delete_student(self):
        selected = self.tree.focus()
        if not selected: return
        student_id = self.tree.item(selected)['values'][0]
        self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()
        self.display_students()

    def update_student(self):
        data = [self.entries[k].get() for k in ["name", "email", "gender", "contact", "attendance", "id"]]
        self.cursor.execute("UPDATE students SET name=?, email=?, gender=?, contact=?, attendance=? WHERE id=?", data)
        self.conn.commit()
        self.display_students()

    def search_students(self):
        query = self.search_entry.get()
        self.cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%'+query+'%',))
        self.display_students(self.cursor.fetchall())

    def get_cursor(self, event):
        """Populate input fields when a row is clicked."""
        cursor_row = self.tree.focus()
        contents = self.tree.item(cursor_row)
        row = contents['values']
        if row:
            for i, k in enumerate(["id", "name", "email", "gender", "contact", "attendance"]):
                self.entries[k].delete(0, tk.END) if hasattr(self.entries[k], 'delete') else None
                self.entries[k].set(row[i]) if hasattr(self.entries[k], 'set') else self.entries[k].insert(0, row[i])

    def clear_fields(self):
        for entry in self.entries.values():
            if hasattr(entry, 'set'): entry.set("")
            else: entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentSystem(root)
    root.mainloop()