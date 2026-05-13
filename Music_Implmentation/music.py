import os
import tkinter as tk
from tkinter import filedialog, ttk
import pygame
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image, ImageTk
import io

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Retro Player")
        self.root.geometry("400x600")
        self.root.configure(bg="#121212")

        # Initialize Pygame Mixer
        pygame.mixer.init()

        self.playlist = []
        self.current_index = 0
        self.is_paused = False

        self.setup_ui()

    def setup_ui(self):
        # Album Art Display
        self.album_art_label = tk.Label(self.root, bg="#1a1a1a", width=300, height=300)
        self.album_art_label.pack(pady=30)
        self.set_default_art()

        # Song Title
        self.song_label = tk.Label(self.root, text="No Song Selected", fg="white", bg="#121212", font=("Arial", 12, "bold"))
        self.song_label.pack()

        # Controls Frame
        ctrl_frame = tk.Frame(self.root, bg="#121212")
        ctrl_frame.pack(pady=20)

        self.play_btn = tk.Button(ctrl_frame, text="▶", command=self.play_pause, width=5, font=("Arial", 14), bg="#1DB954", fg="white")
        self.play_btn.grid(row=0, column=1, padx=10)

        tk.Button(ctrl_frame, text="⏮", command=self.prev_song, bg="#333", fg="white").grid(row=0, column=0)
        tk.Button(ctrl_frame, text="⏭", command=self.next_song, bg="#333", fg="white").grid(row=0, column=2)

        # Volume Slider
        vol_frame = tk.Frame(self.root, bg="#121212")
        vol_frame.pack(pady=10)
        tk.Label(vol_frame, text="🔈", fg="white", bg="#121212").pack(side="left")
        self.volume_slider = ttk.Scale(vol_frame, from_=0, to=1, orient="horizontal", command=self.set_volume, length=150)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side="left", padx=5)

        # Playlist Button
        tk.Button(self.root, text="Add Folder to Playlist", command=self.load_folder, bg="#333", fg="white").pack(pady=10)

    def set_default_art(self):
        # Creates a gray placeholder if no album art exists
        placeholder = Image.new('RGB', (300, 300), color='#333333')
        photo = ImageTk.PhotoImage(placeholder)
        self.album_art_label.config(image=photo)
        self.album_art_label.image = photo

    def load_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.playlist = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".mp3")]
            if self.playlist:
                self.current_index = 0
                self.load_song()

    def load_song(self):
        song_path = self.playlist[self.current_index]
        pygame.mixer.music.load(song_path)
        
        # Display Song Name
        self.song_label.config(text=os.path.basename(song_path))
        
        # Extract Album Art using Mutagen
        try:
            audio = MP3(song_path, ID3=ID3)
            # APIC is the tag for album art
            art_data = audio.tags.getall("APIC")[0].data
            img = Image.open(io.BytesIO(art_data))
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.album_art_label.config(image=photo)
            self.album_art_label.image = photo
        except Exception:
            self.set_default_art()

    def play_pause(self):
        if not self.playlist: return

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            self.play_btn.config(text="⏸")
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_btn.config(text="⏸")
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.config(text="▶")

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_song()
            pygame.mixer.music.play()
            self.play_btn.config(text="⏸")

    def prev_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_song()
            pygame.mixer.music.play()
            self.play_btn.config(text="⏸")

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()