import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class Notepad:
    def __init__(self, width=800, height=600):
        """
        Initializes the Notepad application.
        
        Args:
            width (int): The width of the application window.
            height (int): The height of the application window.
        """
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
        """
        Creates the application menu.
        """
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
        """
        Quits the application.
        """
        self.root.destroy()

    def show_about(self):
        """
        Displays the about dialog.
        """
        messagebox.showinfo("Notepad", "Mrinal Verma")

    def open_file(self):
        """
        Opens a file.
        """
        self.file = filedialog.askopenfilename(defaultextension=".txt",
                                                       filetypes=[("All Files", "*.*"),
                                                                   ("Text Documents", "*.txt")])
        if self.file:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.text_area.delete(1.0, "end")
            try:
                with open(self.file, "r") as file:
                    self.text_area.insert(1.0, file.read())
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def new_file(self):
        """
        Creates a new file.
        """
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(1.0, "end")

    def save_file(self):
        """
        Saves the file.
        """
        if self.file is None:
            self.file = filedialog.asksaveasfilename(initialfile='Untitled.txt',
                                                             defaultextension=".txt",
                                                             filetypes=[("All Files", "*.*"),
                                                                         ("Text Documents", "*.txt")])
            if self.file:
                try:
                    with open(self.file, "w") as file:
                        file.write(self.text_area.get(1.0, "end"))
                    self.root.title(os.path.basename(self.file) + " - Notepad")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            try:
                with open(self.file, "w") as file:
                    file.write(self.text_area.get(1.0, "end"))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def cut(self):
        """
        Cuts the selected text.
        """
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        """
        Copies the selected text.
        """
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        """
        Pastes the text from the clipboard.
        """
        self.text_area.event_generate("<<Paste>>")

    def find(self):
        """
        Finds the text in the text area.
        """
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
        """
        Replaces the text in the text area.
        """
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
        """
        Runs the application.
        """
        self.root.mainloop()


if __name__ == "__main__":
    notepad = Notepad(width=600, height=400)
    notepad.run()
