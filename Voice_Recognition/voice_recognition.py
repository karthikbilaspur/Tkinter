import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import threading

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Voice Assistant")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")

        # Initialize Text-to-Speech
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id) # 0 for male, 1 for female

        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()

        self.setup_ui()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="🎙️ AI Assistant", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50").pack(pady=20)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self.root, width=40, height=15, bg="#34495e", fg="white", font=("Arial", 10))
        self.log_area.pack(pady=10, padx=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Idle", fg="#bdc3c7", bg="#2c3e50")
        self.status_label.pack()

        # Control Button
        self.mic_btn = tk.Button(self.root, text="Listen", command=self.start_listening_thread, 
                                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), width=15)
        self.mic_btn.pack(pady=20)

    def speak(self, text):
        self.log_area.insert(tk.END, f"Assistant: {text}\n")
        self.log_area.see(tk.END)
        self.engine.say(text)
        self.engine.runAndWait()

    def start_listening_thread(self):
        # Run listening in a thread so the UI doesn't freeze
        threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        with sr.Microphone() as source:
            self.status_label.config(text="Listening...", fg="#2ecc71")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.recognizer.listen(source)

        try:
            self.status_label.config(text="Processing...", fg="#f1c40f")
            command = self.recognizer.recognize_google(audio).lower()
            self.log_area.insert(tk.END, f"You: {command}\n")
            self.execute_command(command)
        except Exception:
            self.speak("Sorry, I didn't catch that.")
        
        self.status_label.config(text="Idle", fg="#bdc3c7")

    def execute_command(self, command):
        # 1. Open Web Search
        if "search" in command:
            search_query = command.replace("search", "").strip()
            self.speak(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        # 2. Open Specific Apps (Example: Notepad)
        elif "open notepad" in command:
            self.speak("Opening Notepad")
            os.system("notepad.exe")

        # 3. Open Website
        elif "open youtube" in command:
            self.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # 4. Greeting
        elif "hello" in command:
            self.speak("Hello! How can I help you today?")

        else:
            self.speak("I understand the command, but I don't have an action for it yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistant(root)
    root.mainloop()