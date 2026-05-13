import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import sqlite3
import threading
import time
from datetime import datetime

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus Clipboard")
        self.root.geometry("450x600")
        self.root.configure(bg="#1e1e2e")

        self.last_item = ""
        self.db_init()
        self.setup_ui()
        
        # Start the background listener
        self.running = True
        self.thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.thread.start()
        
        self.load_history()

    def db_init(self):
        self.conn = sqlite3.connect("clipboard_history.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS history 
                            (id INTEGER PRIMARY KEY, content TEXT, timestamp TEXT, pinned INTEGER DEFAULT 0)""")
        self.conn.commit()

    def setup_ui(self):
        # Search Bar
        search_frame = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        search_frame.pack(fill="x", padx=15)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.load_history(self.search_var.get()))
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg="#313244", 
                                fg="white", insertbackground="white", relief="flat", font=("Arial", 11))
        search_entry.pack(fill="x", ipady=8)
        search_entry.insert(0, "Search history...")

        # History List (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e2e", foreground="white", fieldbackground="#1e1e2e", rowheight=40)
        style.map("Treeview", background=[('selected', '#89b4fa')])

        self.tree = ttk.Treeview(self.root, columns=("content", "time"), show="headings")
        self.tree.heading("content", text="Content Snippet")
        self.tree.heading("time", text="Time")
        self.tree.column("content", width=300)
        self.tree.column("time", width=100)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree.bind("<Double-1>", self.copy_selected)
        
        # Controls
        btn_frame = tk.Frame(self.root, bg="#1e1e2e", pady=10)
        btn_frame.pack(fill="x", padx=15)
        
        tk.Button(btn_frame, text="Pin Item", command=self.toggle_pin, bg="#fab387", relief="flat").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear All", command=self.clear_history, bg="#f38ba8", relief="flat").pack(side="right", padx=5)

    def monitor_clipboard(self):
        """Background loop to watch the OS clipboard."""
        while self.running:
            try:
                current_item = pyperclip.paste()
                if current_item != self.last_item and current_item.strip() != "":
                    self.save_to_db(current_item)
                    self.last_item = current_item
                    self.root.after(0, self.load_history)
            except Exception as e:
                print(f"Clipboard Error: {e}")
            time.sleep(1)

    def save_to_db(self, content):
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Prevent saving the exact same content twice
        self.cur.execute("SELECT id FROM history WHERE content = ?", (content,))
        if not self.cur.fetchone():
            self.cur.execute("INSERT INTO history (content, timestamp) VALUES (?, ?)", (content, timestamp))
            self.conn.commit()

    def load_history(self, filter_text=""):
        self.tree.delete(*self.tree.get_children())
        if filter_text and filter_text != "Search history...":
            self.cur.execute("SELECT content, timestamp, pinned FROM history WHERE content LIKE ? ORDER BY pinned DESC, id DESC", 
                             ('%'+filter_text+'%',))
        else:
            self.cur.execute("SELECT content, timestamp, pinned FROM history ORDER BY pinned DESC, id DESC LIMIT 50")
        
        for row in self.cur.fetchall():
            prefix = "📌 " if row[2] else ""
            display_text = (row[0][:50] + '..') if len(row[0]) > 50 else row[0]
            self.tree.insert("", "end", values=(prefix + display_text, row[1]), tags=(row[0],))

    def copy_selected(self, event):
        selected = self.tree.focus()
        if selected:
            # We store the full text in the 'tags' property to avoid truncating it
            full_text = self.tree.item(selected)['tags'][0]
            pyperclip.copy(full_text)
            self.last_item = full_text # Prevent re-saving it immediately
            messagebox.showinfo("Copied", "Item copied back to clipboard!")

    def toggle_pin(self):
        selected = self.tree.focus()
        if selected:
            full_text = self.tree.item(selected)['tags'][0]
            self.cur.execute("UPDATE history SET pinned = CASE WHEN pinned = 1 THEN 0 ELSE 1 END WHERE content = ?", (full_text,))
            self.conn.commit()
            self.load_history()

    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all unpinned history?"):
            self.cur.execute("DELETE FROM history WHERE pinned = 0")
            self.conn.commit()
            self.load_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardManager(root)
    root.mainloop()