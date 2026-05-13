import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro Inventory & Billing")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f5f6fa")

        self.db_init()
        self.setup_ui()
        self.update_product_list()

    def db_init(self):
        self.conn = sqlite3.connect("inventory.db")
        self.cur = self.conn.cursor()
        # Table for products
        self.cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            category TEXT,
                            price REAL,
                            qty INTEGER,
                            threshold INTEGER)""")
        self.conn.commit()

    def setup_ui(self):
        # --- LEFT: Product Management ---
        manage_frame = tk.LabelFrame(self.root, text="Product Management", padx=10, pady=10)
        manage_frame.place(x=20, y=20, width=350, height=600)

        fields = [("Name", "name"), ("Category", "cat"), ("Price", "price"), 
                  ("Quantity", "qty"), ("Stock Alert Level", "threshold")]
        self.entries = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(manage_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(manage_frame)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[key] = entry

        tk.Button(manage_frame, text="Add/Update Product", bg="#4cd137", command=self.save_product).grid(row=5, columnspan=2, pady=20)

        # --- RIGHT TOP: Inventory View & Alerts ---
        view_frame = tk.LabelFrame(self.root, text="Stock Overview", padx=10, pady=10)
        view_frame.place(x=390, y=20, width=680, height=300)

        self.tree = ttk.Treeview(view_frame, columns=("id", "name", "price", "qty", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product")
        self.tree.heading("price", text="Price")
        self.tree.heading("qty", text="Stock")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill="both", expand=True)

        # --- RIGHT BOTTOM: Billing System ---
        bill_frame = tk.LabelFrame(self.root, text="Quick Billing", padx=10, pady=10)
        bill_frame.place(x=390, y=330, width=680, height=290)

        tk.Label(bill_frame, text="Select Product ID:").grid(row=0, column=0)
        self.bill_id = tk.Entry(bill_frame, width=10)
        self.bill_id.grid(row=0, column=1, padx=5)

        tk.Label(bill_frame, text="Qty:").grid(row=0, column=2)
        self.bill_qty = tk.Entry(bill_frame, width=10)
        self.bill_qty.grid(row=0, column=3, padx=5)

        tk.Button(bill_frame, text="Generate Bill", bg="#0097e6", fg="white", command=self.generate_bill).grid(row=0, column=4, padx=10)

        self.bill_area = tk.Text(bill_frame, font=("Courier", 10))
        self.bill_area.grid(row=1, columnspan=5, pady=10, sticky="nsew")

    # --- Core Logic ---

    def save_product(self):
        vals = (self.entries['name'].get(), self.entries['cat'].get(), 
                self.entries['price'].get(), self.entries['qty'].get(), self.entries['threshold'].get())
        
        if "" in vals:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        self.cur.execute("INSERT INTO inventory (name, category, price, qty, threshold) VALUES (?,?,?,?,?)", vals)
        self.conn.commit()
        self.update_product_list()
        messagebox.showinfo("Success", "Product Added")

    def update_product_list(self):
        self.tree.delete(*self.tree.get_children())
        self.cur.execute("SELECT id, name, price, qty, threshold FROM inventory")
        for row in self.cur.fetchall():
            # Stock Alert Logic
            status = "OK"
            if row[3] <= row[4]:
                status = "LOW STOCK"
            
            self.tree.insert("", "end", values=(row[0], row[1], f"${row[2]}", row[3], status))

    def generate_bill(self):
        pid = self.bill_id.get()
        qty_needed = int(self.bill_qty.get())

        self.cur.execute("SELECT name, price, qty, threshold FROM inventory WHERE id=?", (pid,))
        product = self.cur.fetchone()

        if product:
            name, price, current_qty, threshold = product
            if current_qty >= qty_needed:
                new_qty = current_qty - qty_needed
                self.cur.execute("UPDATE inventory SET qty=? WHERE id=?", (new_qty, pid))
                self.conn.commit()
                
                # Create receipt text
                total = price * qty_needed
                receipt = f"--- INVOICE ---\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                receipt += f"Item: {name}\nQty: {qty_needed}\nTotal: ${total:.2f}\n--------------"
                self.bill_area.delete("1.0", tk.END)
                self.bill_area.insert(tk.END, receipt)
                
                self.update_product_list()
                
                # Check for alert after sale
                if new_qty <= threshold:
                    messagebox.showwarning("Stock Alert", f"Warning: {name} is now low on stock!")
            else:
                messagebox.showerror("Error", "Insufficient Stock")
        else:
            messagebox.showerror("Error", "Product Not Found")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystem(root)
    root.mainloop()