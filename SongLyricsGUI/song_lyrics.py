import tkinter as tk
from tkinter import messagebox, filedialog
from lyrics_extractor import SongLyrics
import os
import requests

class SongLyricsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Lyrics Retrieval")
        self.root.configure(bg='light grey')

        # Create API keys file
        self.api_keys_file = "api_keys.txt"
        self.api_keys = self.load_api_keys()

        # Create UI elements
        self.create_ui()

    def load_api_keys(self):
        """Load API keys from file"""
        if os.path.exists(self.api_keys_file):
            with open(self.api_keys_file, "r") as f:
                api_keys = [line.strip() for line in f.readlines()]
                if len(api_keys) != 2:
                    messagebox.showerror("Error", "Invalid API keys file")
                    return None
                return api_keys
        else:
            messagebox.showerror("Error", "API keys file not found")
            return None

    def create_ui(self):
        """Create UI elements"""
        # Create labels and entry fields
        tk.Label(self.root, text="Enter Song name :", bg="light grey").grid(row=0, sticky=tk.W)
        self.song_name_entry = tk.Entry(self.root, width=50)
        self.song_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Select Language:", bg="light grey").grid(row=1, sticky=tk.W)
        self.language_var = tk.StringVar(self.root)
        self.language_var.set("English")  # default value
        language_option = tk.OptionMenu(self.root, self.language_var, "English", "Spanish", "French")
        language_option.grid(row=1, column=1)

        tk.Label(self.root, text="Select Provider:", bg="light grey").grid(row=2, sticky=tk.W)
        self.provider_var = tk.StringVar(self.root)
        self.provider_var.set("MetroLyrics")  # default value
        provider_option = tk.OptionMenu(self.root, self.provider_var, "MetroLyrics", "AZLyrics", "LyricsFreak")
        provider_option.grid(row=2, column=1)

        # Create buttons
        tk.Button(self.root, text="Show", command=self.get_lyrics, bg="Blue").grid(row=3, column=0)
        tk.Button(self.root, text="Save", command=self.save_lyrics, bg="Blue").grid(row=3, column=1)
        tk.Button(self.root, text="Share", command=self.share_lyrics, bg="Blue").grid(row=3, column=2)

        # Create label for lyrics display
        self.lyrics_label = tk.Label(self.root, text="", bg="light grey", wraplength=400)
        self.lyrics_label.grid(row=4, column=0, columnspan=3)

    def get_lyrics(self):
        """Get song lyrics"""
        song_name = self.song_name_entry.get()
        language = self.language_var.get()
        provider = self.provider_var.get()
        if not song_name:
            self.lyrics_label.config(text="Please enter a song name")
            return

        try:
            extract_lyrics = SongLyrics(self.api_keys[0], self.api_keys[1])
            lyrics = extract_lyrics.get_lyrics(song_name, language, provider)
            self.lyrics_label.config(text=lyrics["lyrics"])
        except Exception as e:
            self.lyrics_label.config(text="Error: " + str(e))

    def save_lyrics(self):
        """Save lyrics to a file"""
        lyrics = self.lyrics_label.cget("text")
        if not lyrics:
            messagebox.showerror("Error", "No lyrics to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "w") as f:
            f.write(lyrics)

    def share_lyrics(self):
        """Share lyrics on social media"""
        lyrics = self.lyrics_label.cget("text")
        if not lyrics:
            messagebox.showerror("Error", "No lyrics to share")
            return

        # Share on Twitter
        twitter_url = f"https://twitter.com/intent/tweet?text={lyrics}"
        requests.get(twitter_url)

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SongLyricsApp(root)
    app.run()