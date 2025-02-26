import sounddevice as sd
import soundfile as sf
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
import threading
import pyaudio
import wave
import audioop
import math

class VoiceRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("300x250")
        self.label = Label(root, text="Voice Recorder")
        self.label.grid(row=0, column=0, columnspan=3)
        self.status_label = Label(root, text="Not Recording")
        self.status_label.grid(row=1, column=0, columnspan=3)
        self.record_button = Button(root, text="Start Recording", command=self.start_recording)
        self.record_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.stop_button = Button(root, text="Stop Recording", command=self.stop_recording, state=DISABLED)
        self.stop_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self.pause_button = Button(root, text="Pause Recording", command=self.pause_recording, state=DISABLED)
        self.pause_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.resume_button = Button(root, text="Resume Recording", command=self.resume_recording, state=DISABLED)
        self.resume_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        self.save_button = Button(root, text="Save Recording", command=self.save_recording, state=DISABLED)
        self.save_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        self.play_button = Button(root, text="Play Recording", command=self.play_recording, state=DISABLED)
        self.play_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
        self.exit_button = Button(root, text="Exit", command=root.destroy)
        self.exit_button.grid(row=8, column=0, columnspan=3, padx=5, pady=5)
        self.recording = False
        self.paused = False
        self.myrecording = None
        self.fs = 48000  # Sampling frequency
        self.duration = 5  # Recording duration in seconds
        self.recording_time_label = Label(root, text="Recording Time: 5 seconds")
        self.recording_time_label.grid(row=9, column=0, columnspan=3)
        self.audio_format_label = Label(root, text="Audio Format: FLAC")
        self.audio_format_label.grid(row=10, column=0, columnspan=3)
        self.audio_quality_label = Label(root, text="Audio Quality: High")
        self.audio_quality_label.grid(row=11, column=0, columnspan=3)

    def start_recording(self):
        self.recording = True
        self.paused = False
        self.status_label.config(text="Recording...")
        self.record_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.pause_button.config(state=NORMAL)
        self.save_button.config(state=DISABLED)
        self.play_button.config(state=DISABLED)
        threading.Thread(target=self.record_audio).start()

    def record_audio(self):
        self.myrecording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2)
        sd.wait()  # Wait for recording to finish
        self.stop_recording()

    def stop_recording(self):
        self.recording = False
        self.paused = False
        self.status_label.config(text="Not Recording")
        self.record_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        self.pause_button.config(state=DISABLED)
        self.resume_button.config(state=DISABLED)
        self.save_button.config(state=NORMAL)
        self.play_button.config(state=NORMAL)

    def pause_recording(self):
        self.paused = True
        self.status_label.config(text="Paused")
        self.pause_button.config(state=DISABLED)
        self.resume_button.config(state=NORMAL)

    def resume_recording(self):
        self.paused = False
        self.status_label.config(text="Recording...")
        self.pause_button.config(state=NORMAL)
        self.resume_button.config(state=DISABLED)

    def save_recording(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".flac", filetypes=[("Audio Files", "*.flac")])
        if file_path:
            sf.write(file_path, self.myrecording, self.fs)
            messagebox.showinfo("Recording Saved", f"Recording saved to {file_path}")
        else:
            messagebox.showinfo("Recording Not Saved", "Recording not saved")

    def play_recording(self):
        try:
            sd.play(self.myrecording, self.fs)
            sd.wait()  # Wait for playback to finish
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def set_recording_time(self):
        self.duration = simpledialog.askinteger("Set Recording Time", "Enter recording time in seconds")
        self.recording_time_label.config(text=f"Recording Time: {self.duration} seconds")

    def set_audio_format(self):
        audio_format = simpledialog.askstring("Set Audio Format", "Enter audio format (e.g. FLAC, WAV, MP3)")
        self.audio_format_label.config(text=f"Audio Format: {audio_format}")

    def set_audio_quality(self):
        audio_quality = simpledialog.askstring("Set Audio Quality", "Enter audio quality (e.g. High, Medium, Low)")
        self.audio_quality_label.config(text=f"Audio Quality: {audio_quality}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = VoiceRecorder(root)
    app.run()