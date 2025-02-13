"""
Voice Recorder Application

This application allows users to record, play back, and save audio recordings.
"""

import sounddevice as sd
import soundfile as sf
from tkinter import *
from tkinter import filedialog, messagebox

class VoiceRecorder:
    """
    Voice Recorder Class

    This class represents the voice recorder application.
    It contains methods for recording, playing back, and saving audio recordings.
    """

    def __init__(self, root):
        """
        Initializes the Voice Recorder Application

        Args:
            root (Tk): The root window of the application
        """
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
        self.save_button = Button(root, text="Save Recording", command=self.save_recording, state=DISABLED)
        self.save_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.play_button = Button(root, text="Play Recording", command=self.play_recording, state=DISABLED)
        self.play_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
        self.exit_button = Button(root, text="Exit", command=root.destroy)
        self.exit_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        self.recording = False
        self.myrecording = None
        self.fs = 48000  # Sampling frequency
        self.duration = 5  # Recording duration in seconds
        self.recording_time_label = Label(root, text="Recording Time: 5 seconds")
        self.recording_time_label.grid(row=7, column=0, columnspan=3)

    def start_recording(self):
        """
        Starts Recording Audio

        Records audio for the specified duration and sampling frequency.
        """
        # Record audio
        self.myrecording = sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=2)
        self.recording = True
        self.status_label.config(text="Recording...")
        self.record_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)
        self.save_button.config(state=DISABLED)
        self.play_button.config(state=DISABLED)
        sd.wait()  # Wait for recording to finish

    def stop_recording(self):
        """
        Stops Recording Audio

        Stops the recording and updates the GUI accordingly.
        """
        self.recording = False
        self.status_label.config(text="Not Recording")
        self.record_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)
        self.save_button.config(state=NORMAL)
        self.play_button.config(state=NORMAL)

    def save_recording(self):
        """
        Saves the Recorded Audio

        Saves the recorded audio to a file selected by the user.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".flac", filetypes=[("Audio Files", "*.flac")])
        if file_path:
            sf.write(file_path, self.myrecording, self.fs)
            messagebox.showinfo("Recording Saved", f"Recording saved to {file_path}")
        else:
            messagebox.showinfo("Recording Not Saved", "Recording not saved")

    def play_recording(self):
        """
        Plays Back the Recorded Audio

        Plays back the recorded audio using the sounddevice library.
        """
        try:
            sd.play(self.myrecording, self.fs)
            sd.wait()  # Wait for playback to finish
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        """
        Runs the Voice Recorder Application

        Starts the main event loop of the application.
        """
        self.root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = VoiceRecorder(root)
    app.run()