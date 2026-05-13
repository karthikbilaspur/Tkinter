import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Library Manager")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f2f5")

        self.db_init()
        self.setup_ui()
        self.refresh_tables()

    def db_init(self):
        self.conn = sqlite3.connect("library.db")
        self.cur = self.conn.cursor()
        # Books table
        self.cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, status TEXT)")
        # Users & Transactions table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS issued_books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            book_id INTEGER,
                            user_name TEXT,
                            issue_date TEXT,
                            due_date TEXT)""")
        self.conn.commit()

    def setup_ui(self):
        # --- TOP: Book Entry & Management ---
        top_frame = tk.LabelFrame(self.root, text="Book Management", padx=10, pady=10)
        top_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(top_frame, text="Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(top_frame)
        self.title_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Author:").grid(row=0, column=2)
        self.author_entry = tk.Entry(top_frame)
        self.author_entry.grid(row=0, column=3, padx=5)

        tk.Button(top_frame, text="Add Book", command=self.add_book, bg="#2ecc71", fg="white").grid(row=0, column=4, padx=10)

        # --- MIDDLE: The Dashboard (Two Tables) ---
        mid_frame = tk.Frame(self.root)
        mid_frame.pack(fill="both", expand=True, padx=20)

        # Available Books Table
        self.book_tree = ttk.Treeview(mid_frame, columns=("id", "title", "author", "status"), show="headings")
        self.book_tree.heading("id", text="ID")
        self.book_tree.heading("title", text="Title")
        self.book_tree.heading("author", text="Author")
        self.book_tree.heading("status", text="Status")
        self.book_tree.pack(side="left", fill="both", expand=True, padx=5)

        # Issued Books Table
        self.issue_tree = ttk.Treeview(mid_frame, columns=("bid", "user", "due"), show="headings")
        self.issue_tree.heading("bid", text="Book ID")
        self.issue_tree.heading("user", text="User")
        self.issue_tree.heading("due", text="Due Date")
        self.issue_tree.pack(side="right", fill="both", expand=True, padx=5)

        # --- BOTTOM: Issue/Return Controls ---
        bottom_frame = tk.LabelFrame(self.root, text="Issue / Return Actions", padx=10, pady=10)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(bottom_frame, text="User Name:").grid(row=0, column=0)
        self.user_entry = tk.Entry(bottom_frame)
        self.user_entry.grid(row=0, column=1, padx=5)

        tk.Button(bottom_frame, text="Issue Selected", command=self.issue_book, bg="#3498db", fg="white").grid(row=0, column=2, padx=10)
        tk.Button(bottom_frame, text="Return Selected", command=self.return_book, bg="#e67e22", fg="white").grid(row=0, column=3, padx=10)

    # --- Logic ---

    def add_book(self):
        t, a = self.title_entry.get(), self.author_entry.get()
        if t and a:
            self.cur.execute("INSERT INTO books (title, author, status) VALUES (?,?,?)", (t, a, "Available"))
            self.conn.commit()
            self.refresh_tables()
            messagebox.showinfo("Success", "Book added to library")

    def issue_book(self):
        selected = self.book_tree.focus()
        user = self.user_entry.get()
        if not selected or not user:
            messagebox.showwarning("Error", "Select a book and enter user name")
            return
        
        book_data = self.book_tree.item(selected)['values']
        if book_data[3] == "Issued":
            messagebox.showerror("Error", "Book is already issued")
            return

        # Calculate dates
        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        self.cur.execute("INSERT INTO issued_books (book_id, user_name, issue_date, due_date) VALUES (?,?,?,?)",
                         (book_data[0], user, issue_date, due_date))
        self.cur.execute("UPDATE books SET status='Issued' WHERE id=?", (book_data[0],))
        self.conn.commit()
        self.refresh_tables()

    def return_book(self):
        selected = self.issue_tree.focus()
        if not selected: return
        
        book_id = self.issue_tree.item(selected)['values'][0]
        self.cur.execute("SELECT due_date FROM issued_books WHERE book_id=?", (book_id,))
        due_date_str = self.cur.fetchone()[0]
        
        # Fine Calculation
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        today = datetime.now()
        fine = 0
        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * 2 # $2 per day
            messagebox.showinfo("Fine Alert", f"Book is late! Fine: ${fine}")

        self.cur.execute("DELETE FROM issued_books WHERE book_id=?", (book_id,))
        self.cur.execute("UPDATE books SET status='Available' WHERE id=?", (book_id,))
        self.conn.commit()
        self.refresh_tables()

    def refresh_tables(self):
        # Update Available Table
        self.book_tree.delete(*self.book_tree.get_children())
        self.cur.execute("SELECT * FROM books")
        for row in self.cur.fetchall(): self.book_tree.insert("", "end", values=row)

        # Update Issued Table
        self.issue_tree.delete(*self.issue_tree.get_children())
        self.cur.execute("SELECT book_id, user_name, due_date FROM issued_books")
        for row in self.cur.fetchall(): self.issue_tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()