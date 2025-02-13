import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from time import sleep
import webbrowser
import os

class UnitConverterApp:
    def __init__(self):
        self.wind = tk.Tk()
        self.wind.deiconify()
        self.wind.resizable(0, 0)
        self.wind.configure(bg="#008080")
        self.wind.title("Unit Converter")
        icon = tk.PhotoImage(file=r"convert.png")
        self.wind.iconphoto(False, icon)
        self.center(self.wind, 500, 230)

        self.create_widgets()

        self.wind.mainloop()

    def create_widgets(self):
        """Create UI widgets"""
        entry = tk.Label(self.wind, bg="#008080", fg="white",
                      text="Welcome to Unit Converter!",
                      font=("Footlight MT Light", 15, "bold"))
        entry.place(x=50, y=30, width=410, height=30)

        self.load = Progressbar(self.wind, orient=tk.HORIZONTAL,
                                length=250,
                                mode='indeterminate')

        self.start = tk.Button(self.wind, bg="#f5f5f5", fg="black",
                            text="START", command=self.loading)
        self.start.place(x=200, y=90,
                        width=80, height=30)

        follow = tk.Label(self.wind, bg="#008080", fg="white",
                       text="Follow Me On",
                       font=("Helvetica", 12, "bold"))
        follow.place(x=186, y=150, width=104,
                     height=20)

        self.git = tk.PhotoImage(file=r'gforg.png')
        github = tk.Button(self.wind, image=self.git, bg="white",
                        relief=tk.FLAT,
                        command=lambda: self.open_url("https://github.com/your-username"),
                        cursor="hand2")
        github.place(x=110, y=190, width=30,
                     height=30)

        self.instag = tk.PhotoImage(file=r'ins.png')
        insta = tk.Button(self.wind, image=self.instag,
                       bg="#008080", relief=tk.FLAT,
                       command=lambda: self.open_url("https://www.instagram.com/your-username"),
                       cursor="hand2")
        insta.place(x=190, y=190, width=30,
                    height=30)

        self.fcb = tk.PhotoImage(file=r'fb.png')
        fb = tk.Button(self.wind, image=self.fcb, bg="white",
                    relief=tk.FLAT,
                    command=lambda: self.open_url("https://www.facebook.com/your-username"),
                    cursor="hand2")
        fb.place(x=270, y=190, width=30,
                 height=30)

        self.tweet = tk.PhotoImage(file=r'twitter.png')
        twitter = tk.Button(self.wind, image=self.tweet,
                         bg="white", relief=tk.FLAT,
                         command=lambda: self.open_url("https://twitter.com/your-username"),
                         cursor="hand2")
        twitter.place(x=350, y=190,
                      width=30, height=30)

    def open_url(self, url):
        """Open a URL in the default browser"""
        webbrowser.open(url)

    def loading(self):
        """Simulate a loading animation"""
        self.start.place(x=0, y=0, width=0,
                         height=0)
        self.load.place(x=120, y=100)
        self.wind.update()
        c = 0
        while c < 100:
            self.load['value'] = c
            self.wind.update()
            sleep(0.01)
            c += 1
        self.shift("Length")

    def center(self, wind, width, height):
        """Center the window on the screen"""
        screen_width = wind.winfo_screenwidth()
        screen_height = wind.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        wind.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def shift(self, unit):
        # Calling Shift function
        # to initialise converter window.
        pass

if __name__ == "__main__":
    intro = UnitConverterApp()