import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import time
from plyer import notification

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority Task Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f6fa")

        self.tasks = []
        self.setup_ui()
        
        # Start the background notification checker
        threading.Thread(target=self.check_notifications, daemon=True).start()

    def setup_ui(self):
        # --- Input Section ---
        input_frame = tk.LabelFrame(self.root, text="New Task", padx=10, pady=10)
        input_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(input_frame, text="Task:").grid(row=0, column=0)
        self.task_entry = tk.Entry(input_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Priority:").grid(row=0, column=2)
        self.priority_cb = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], width=10)
        self.priority_cb.set("Medium")
        self.priority_cb.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Due Time (HH:MM):").grid(row=0, column=4)
        self.time_entry = tk.Entry(input_frame, width=10)
        self.time_entry.insert(0, datetime.now().strftime("%H:%M"))
        self.time_entry.grid(row=0, column=5, padx=5)

        tk.Button(input_frame, text="Add Task", bg="#00a8ff", fg="white", command=self.add_task).grid(row=0, column=6, padx=10)

        # --- Dashboard Table ---
        self.tree = ttk.Treeview(self.root, columns=("task", "priority", "due", "status"), show="headings")
        self.tree.heading("task", text="Task Name")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("due", text="Due Time")
        self.tree.heading("status", text="Status")
        
        # Color tags for priorities
        self.tree.tag_configure('High', foreground="#e84118")
        self.tree.tag_configure('Medium', foreground="#fbc531")
        self.tree.tag_configure('Low', foreground="#4cd137")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def add_task(self):
        name = self.task_entry.get()
        prio = self.priority_cb.get()
        due = self.time_entry.get()

        if name and due:
            task_data = {"name": name, "prio": prio, "due": due, "notified": False}
            self.tasks.append(task_data)
            self.tree.insert("", "end", values=(name, prio, due, "Pending"), tags=(prio,))
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")

    def check_notifications(self):
        """Background loop to check for due dates."""
        while True:
            current_time = datetime.now().strftime("%H:%M")
            for task in self.tasks:
                if task['due'] == current_time and not task['notified']:
                    # Trigger OS Notification
                    notification.notify(
                        title=f"🕒 Task Reminder: {task['prio']} Priority",
                        message=f"It's time for: {task['name']}",
                        app_icon=None,
                        timeout=10,
                    )
                    task['notified'] = True
                    self.update_status_ui(task['name'])
            
            time.sleep(30) # Check every 30 seconds

    def update_status_ui(self, task_name):
        # Find the row in treeview and update status to 'Alerted'
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == task_name:
                self.tree.set(item, column="status", value="NOTIFIED")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()