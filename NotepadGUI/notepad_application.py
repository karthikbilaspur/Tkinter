import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class Notepad:
    def __init__(self, width=800, height=600):
        self.root = tk.Tk()
        self.root.title("Untitled - Notepad")
        self.root.geometry(f"{width}x{height}")
        self.text_area = tk.Text(self.root)
        self.text_area.pack(fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        self.file = None
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit_application)
        editmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Cut", command=self.cut)
        editmenu.add_command(label="Copy", command=self.copy)
        editmenu.add_command(label="Paste", command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="Find", command=self.find)
        editmenu.add_command(label="Replace", command=self.replace)
        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About Notepad", command=self.show_about)

    def quit_application(self):
        self.root.destroy()

    def show_about(self):
        messagebox.showinfo("Notepad", "Mrinal Verma")

    def open_file(self):
        self.file = filedialog.askopenfilename(defaultextension=".txt",
                                                       filetypes=[("All Files", "*.*"),
                                                                   ("Text Documents", "*.txt")])
        if self.file:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.text_area.delete(1.0, "end")
            with open(self.file, "r") as file:
                self.text_area.insert(1.0, file.read())

    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(1.0, "end")

    def save_file(self):
        if self.file is None:
            self.file = filedialog.asksaveasfilename(initialfile='Untitled.txt',
                                                             defaultextension=".txt",
                                                             filetypes=[("All Files", "*.*"),
                                                                         ("Text Documents", "*.txt")])
            if self.file:
                with open(self.file, "w") as file:
                    file.write(self.text_area.get(1.0, "end"))
                self.root.title(os.path.basename(self.file) + " - Notepad")
        else:
            with open(self.file, "w") as file:
                file.write(self.text_area.get(1.0, "end"))

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def find(self):
        find_str = simpledialog.askstring("Find", "Enter text to find")
        if find_str:
            self.text_area.tag_remove('match', '1.0', 'end')
            self.text_area.tag_config('match', foreground='red')
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(find_str, start_pos, stopindex='end')
                if not start_pos:
                    break
                lastidx = '%s+%dc' % (start_pos, len(find_str))
                self.text_area.tag_add('match', start_pos, lastidx)
                start_pos = lastidx

    def replace(self):
        find_str = simpledialog.askstring("Find", "Enter text to find")
        replace_str = simpledialog.askstring("Replace", "Enter text to replace")
        if find_str and replace_str:
            self.text_area.tag_remove('match', '1.0', 'end')
            self.text_area.tag_config('match', foreground='red')
            start_pos = '1.0'
            while True:
                start_pos = self.text_area.search(find_str, start_pos, stopindex='end')
                if not start_pos:
                    break
                lastidx = '%s+%dc' % (start_pos, len(find_str))
                self.text_area.delete(start_pos, lastidx)
                self.text_area.insert(start_pos, replace_str)
                start_pos = lastidx

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    notepad = Notepad(width=600, height=400)
    notepad.run()