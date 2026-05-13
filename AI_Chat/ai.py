import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import json
import os

# --- API Wrappers (Placeholders for your keys) ---
# For Ollama, we use the requests library to talk to the local server
import requests

class ChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Omni-Chat AI")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e1e")

        self.history_file = "chat_history.json"
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        # Sidebar for Provider Selection
        self.side_bar = tk.Frame(self.root, bg="#252526", width=150)
        self.side_bar.pack(side="left", fill="y")

        tk.Label(self.side_bar, text="Provider", fg="white", bg="#252526", font=("Arial", 10, "bold")).pack(pady=10)
        self.provider_var = tk.StringVar(value="Ollama")
        providers = [("Ollama", "Ollama"), ("OpenAI", "OpenAI"), ("Gemini", "Gemini")]
        for text, mode in providers:
            tk.Radiobutton(self.side_bar, text=text, variable=self.provider_var, value=mode, 
                           bg="#252526", fg="white", selectcolor="#37373d", activebackground="#252526").pack(anchor="w", px=10)

        # Main Chat Area
        self.main_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.chat_display = scrolledtext.ScrolledText(self.main_frame, bg="#1e1e1e", fg="#d4d4d4", 
                                                      font=("Segoe UI", 11), state='disabled', wrap='word', borderwidth=0)
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Input Area
        input_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
        input_frame.pack(fill="x", side="bottom", padx=10, pady=10)

        self.user_input = tk.Entry(input_frame, bg="#3c3c3c", fg="white", insertbackground="white", font=("Segoe UI", 12), borderwidth=0)
        self.user_input.pack(side="left", fill="x", expand=True, ipady=8)
        self.user_input.bind("<Return>", self.start_chat_thread)

        self.send_btn = tk.Button(input_frame, text="Send", command=self.start_chat_thread, bg="#007acc", fg="white", relief="flat", padx=15)
        self.send_btn.pack(side="right", padx=5)

    def append_chat(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: ", "bold")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        self.save_history(sender, message)

    def start_chat_thread(self, event=None):
        prompt = self.user_input.get()
        if not prompt: return
        
        self.append_chat("You", prompt)
        self.user_input.delete(0, tk.END)
        
        # Run API call in a separate thread so the GUI stays responsive
        threading.Thread(target=self.fetch_response, args=(prompt,), daemon=True).start()

    def fetch_response(self, prompt):
        provider = self.provider_var.get()
        response = "Error connecting to AI."

        try:
            if provider == "Ollama":
                # Defaulting to llama3; ensure Ollama is running locally
                res = requests.post("http://localhost:11434/api/generate", 
                                    json={"model": "llama3", "prompt": prompt, "stream": False})
                response = res.json().get("response", "No response")
            
            # Placeholder logic for OpenAI/Gemini
            elif provider == "OpenAI":
                response = "[Simulated OpenAI Response] Please add your API key logic here."
            elif provider == "Gemini":
                response = "[Simulated Gemini Response] Please add your API key logic here."

        except Exception as e:
            response = f"Connection failed: {str(e)}"
        
        # Use root.after to update GUI from a background thread safely
        self.root.after(0, lambda: self.append_chat("AI", response))

    def save_history(self, sender, message):
        chat_data = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                chat_data = json.load(f)
        
        chat_data.append({"sender": sender, "message": message, "timestamp": str(datetime.now())})
        with open(self.history_file, 'w') as f:
            json.dump(chat_data, f)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                for entry in data:
                    self.append_chat(entry['sender'], entry['message'])

if __name__ == "__main__":
    from datetime import datetime
    root = tk.Tk()
    app = ChatBot(root)
    root.mainloop()