import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import time
import threading
from datetime import datetime

class PomodoroPro:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusFlow Pro")
        self.root.geometry("450x600")
        self.root.configure(bg="#1a1a1a")

        # Constants & State
        self.WORK_TIME = 25 * 60
        self.SHORT_BREAK = 5 * 60
        self.current_time = self.WORK_TIME
        self.is_running = False
        self.timer_type = "Work" # Work or Break

        self.db_init()
        self.setup_ui()
        self.update_stats()

    def db_init(self):
        self.conn = sqlite3.connect("productivity.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS sessions (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            type TEXT,
                            duration_min INTEGER)""")
        self.conn.commit()

    def setup_ui(self):
        # --- Timer Display ---
        self.label_type = tk.Label(self.root, text="FOCUS MODE", font=("Helvetica", 14, "bold"), fg="#ff4757", bg="#1a1a1a")
        self.label_type.pack(pady=(30, 10))

        self.canvas = tk.Canvas(self.root, width=250, height=250, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()
        
        # Draw static background circle
        self.canvas.create_oval(10, 10, 240, 240, outline="#333", width=10)
        # Dynamic progress arc
        self.progress_arc = self.canvas.create_arc(10, 10, 240, 240, start=90, extent=359, outline="#ff4757", width=10, style="arc")
        
        self.time_display = self.canvas.create_text(125, 125, text="25:00", fill="white", font=("Helvetica", 40, "bold"))

        # --- Controls ---
        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=30)

        self.start_btn = tk.Button(btn_frame, text="START", command=self.toggle_timer, bg="#2ed573", fg="white", font=("Arial", 12, "bold"), width=10, relief="flat")
        self.start_btn.grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="RESET", command=self.reset_timer, bg="#333", fg="white", font=("Arial", 12, "bold"), width=10, relief="flat").grid(row=0, column=1, padx=10)

        # --- Statistics ---
        stats_frame = tk.Frame(self.root, bg="#262626", padx=20, pady=20)
        stats_frame.pack(fill="x", side="bottom")

        self.stats_label = tk.Label(stats_frame, text="Today's Stats", font=("Arial", 10, "bold"), fg="#aaa", bg="#262626")
        self.stats_label.pack(anchor="w")

        self.data_label = tk.Label(stats_frame, text="Sessions: 0 | Total: 0m", font=("Arial", 12), fg="white", bg="#262626")
        self.data_label.pack(anchor="w", pady=5)

    # --- Core Logic ---

    def toggle_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text="PAUSE", bg="#ffa502")
            threading.Thread(target=self.run_timer, daemon=True).start()
        else:
            self.is_running = False
            self.start_btn.config(text="RESUME", bg="#2ed573")

    def run_timer(self):
        while self.current_time > 0 and self.is_running:
            time.sleep(1)
            self.current_time -= 1
            self.root.after(0, self.update_ui)
        
        if self.current_time == 0:
            self.is_running = False
            self.handle_session_complete()

    def update_ui(self):
        # Update text
        mins, secs = divmod(self.current_time, 60)
        self.canvas.itemconfig(self.time_display, text=f"{mins:02d}:{secs:02d}")
        
        # Update progress arc
        total = self.WORK_TIME if self.timer_type == "Work" else self.SHORT_BREAK
        extent = (self.current_time / total) * 360
        self.canvas.itemconfig(self.progress_arc, extent=extent)

    def reset_timer(self):
        self.is_running = False
        self.timer_type = "Work"
        self.current_time = self.WORK_TIME
        self.start_btn.config(text="START", bg="#2ed573")
        self.label_type.config(text="FOCUS MODE", fg="#ff4757")
        self.update_ui()

    def handle_session_complete(self):
        if self.timer_type == "Work":
            # Save to DB
            duration = self.WORK_TIME // 60
            self.cur.execute("INSERT INTO sessions (date, type, duration_min) VALUES (?, ?, ?)",
                             (datetime.now().strftime("%Y-%m-%d"), "Work", duration))
            self.conn.commit()
            
            messagebox.showinfo("Break Time!", "Great work! Time for a short break.")
            self.timer_type = "Break"
            self.current_time = self.SHORT_BREAK
            self.label_type.config(text="BREAK MODE", fg="#2ed573")
        else:
            messagebox.showinfo("Focus!", "Break is over. Back to work!")
            self.timer_type = "Work"
            self.current_time = self.WORK_TIME
            self.label_type.config(text="FOCUS MODE", fg="#ff4757")
        
        self.update_stats()
        self.update_ui()
        self.start_btn.config(text="START", bg="#2ed573")

    def update_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cur.execute("SELECT COUNT(*), SUM(duration_min) FROM sessions WHERE date=?", (today,))
        count, total_min = self.cur.fetchone()
        total_min = total_min if total_min else 0
        self.data_label.config(text=f"Sessions: {count} | Total Focus: {total_min}m")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroPro(root)
    root.mainloop()