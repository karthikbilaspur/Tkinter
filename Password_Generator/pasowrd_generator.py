import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import hashlib
import base64
import json
import os
import random
import string

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Vault - Secure Password Manager")
        self.root.geometry("450x550")
        self.root.configure(bg="#1a1a1a")
        
        self.file_path = "vault.json"
        self.key = None
        self.master_hash = "master.hash"
        
        self.setup_ui()
        self.check_first_run()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="🔐 SECURE VAULT", font=("Arial", 18, "bold"), fg="#00ff88", bg="#1a1a1a").pack(pady=20)

        # Input Fields
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(pady=10, padx=20, fill="x")

        tk.Label(frame, text="Website/App:", fg="white", bg="#1a1a1a").grid(row=0, column=0, sticky="w")
        self.site_entry = tk.Entry(frame, width=30)
        self.site_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:", fg="white", bg="#1a1a1a").grid(row=1, column=0, sticky="w")
        self.pass_entry = tk.Entry(frame, width=30)
        self.pass_entry.grid(row=1, column=1, pady=5)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Generate", command=self.generate_password, bg="#333", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Entry", command=self.save_password, bg="#00ff88", fg="black", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Listbox to show saved sites
        self.listbox = tk.Listbox(self.root, width=50, height=10, bg="#222", fg="white", borderwidth=0)
        self.listbox.pack(pady=20, padx=20)
        
        tk.Button(self.root, text="Copy Selected Password", command=self.copy_password, bg="#444", fg="white").pack()

    # --- Core Logic ---

    def check_first_run(self):
        if not os.path.exists(self.master_hash):
            password = simpledialog.askstring("Setup", "Set a Master Password:", show='*')
            if password:
                # Store SHA-256 hash of master password
                with open(self.master_hash, "w") as f:
                    f.write(hashlib.sha256(password.encode()).hexdigest())
                self.derive_key(password)
        else:
            self.login()

    def login(self):
        password = simpledialog.askstring("Login", "Enter Master Password:", show='*')
        if password:
            entered_hash = hashlib.sha256(password.encode()).hexdigest()
            with open(self.master_hash, "r") as f:
                stored_hash = f.read()
            
            if entered_hash == stored_hash:
                self.derive_key(password)
                self.load_list()
            else:
                messagebox.showerror("Denied", "Incorrect Master Password")
                self.root.destroy()

    def derive_key(self, password):
        # Convert password to a 32-byte key for AES (Fernet)
        key = hashlib.sha256(password.encode()).digest()
        self.key = base64.urlsafe_b64encode(key)

    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pwd = "".join(random.sample(chars, 16))
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, pwd)

    def save_password(self):
        site = self.site_entry.get()
        pwd = self.pass_entry.get()
        
        if not site or not pwd:
            return

        # Encrypt the password
        f = Fernet(self.key)
        encrypted_pwd = f.encrypt(pwd.encode()).decode()

        # Load existing, update, and save
        data = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = json.load(file)
        
        data[site] = encrypted_pwd
        with open(self.file_path, "w") as file:
            json.dump(data, file)
            
        messagebox.showinfo("Success", f"Password for {site} saved!")
        self.load_list()

    def load_list(self):
        self.listbox.delete(0, tk.END)
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = json.load(f)
                for site in data:
                    self.listbox.insert(tk.END, site)

    def copy_password(self):
        selection = self.listbox.curselection()
        if not selection: return
        
        site = self.listbox.get(selection[0])
        with open(self.file_path, "r") as f:
            data = json.load(f)
            encrypted_pwd = data[site]
            
        f = Fernet(self.key)
        decrypted_pwd = f.decrypt(encrypted_pwd.encode()).decode()
        
        self.root.clipboard_clear()
        self.root.clipboard_append(decrypted_pwd)
        messagebox.showinfo("Copied", f"Password for {site} copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()