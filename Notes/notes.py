import tkinter as tk
import sqlite3

class StickyNote:
    def __init__(self, note_id=None, content="", x=100, y=100):
        self.root = tk.Toplevel()
        self.root.geometry(f"250x250+{x}+{y}")
        self.root.overrideredirect(True)  # Removes standard title bar
        self.root.attributes("-topmost", True) # Keep notes on top
        self.root.configure(bg="#feff9c")

        self.note_id = note_id
        self.setup_db()
        self.setup_ui(content)
        self.setup_drag()

    def setup_db(self):
        self.conn = sqlite3.connect("sticky_notes.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS notes 
                            (id INTEGER PRIMARY KEY, content TEXT, x INTEGER, y INTEGER)""")
        self.conn.commit()

    def setup_ui(self, content):
        # Custom Title Bar for dragging and buttons
        self.title_bar = tk.Frame(self.root, bg="#f1f1a1", height=30)
        self.title_bar.pack(fill="x")

        # Close Button
        tk.Button(self.title_bar, text="✕", command=self.delete_note, bg="#f1f1a1", 
                  relief="flat", font=("Arial", 10)).pack(side="right", padx=5)
        
        # Add Note Button
        tk.Button(self.title_bar, text="+", command=lambda: StickyNote(), bg="#f1f1a1", 
                  relief="flat", font=("Arial", 12)).pack(side="left", padx=5)

        # Text Area
        self.text_area = tk.Text(self.root, bg="#feff9c", font=("Segoe Print", 12), 
                                 relief="flat", padx=10, pady=10, borderwidth=0)
        self.text_area.insert("1.0", content)
        self.text_area.pack(fill="both", expand=True)
        
        # Autosave binding: Trigger save on every key release
        self.text_area.bind("<KeyRelease>", self.save_note)

    def setup_drag(self):
        # Logic to make the custom title bar draggable
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_bar.bind("<ButtonRelease-1>", self.save_note)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def save_note(self, event=None):
        content = self.text_area.get("1.0", tk.END).strip()
        x = self.root.winfo_x()
        y = self.root.winfo_y()

        if self.note_id is None:
            self.cur.execute("INSERT INTO notes (content, x, y) VALUES (?, ?, ?)", (content, x, y))
            self.note_id = self.cur.lastrowid
        else:
            self.cur.execute("UPDATE notes SET content=?, x=?, y=? WHERE id=?", (content, x, y, self.note_id))
        
        self.conn.commit()

    def delete_note(self):
        if self.note_id:
            self.cur.execute("DELETE FROM notes WHERE id=?", (self.note_id,))
            self.conn.commit()
        self.root.destroy()

def load_saved_notes():
    conn = sqlite3.connect("sticky_notes.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT, x INTEGER, y INTEGER)")
    cur.execute("SELECT * FROM notes")
    saved_notes = cur.fetchall()
    
    if not saved_notes:
        StickyNote() # Start with one empty note
    else:
        for note in saved_notes:
            StickyNote(note_id=note[0], content=note[1], x=note[2], y=note[3])

if __name__ == "__main__":
    main_root = tk.Tk()
    main_root.withdraw() # Hide the main hidden root window
    load_saved_notes()
    main_root.mainloop()