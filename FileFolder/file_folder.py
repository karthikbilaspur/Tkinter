import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title('File Explorer')
        self.root.geometry("500x600")
        self.root.config(background="white")

        # Create a File Explorer label
        self.label_file_explorer = ttk.Label(self.root, 
                                            text="File Explorer using Tkinter",
                                            font=("Arial", 14))
        self.label_file_explorer.grid(column=1, row=1, padx=10, pady=10)

        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(column=1, row=2, padx=10, pady=10)

        # Create a button to browse files
        self.button_explore = ttk.Button(self.button_frame, 
                                         text="Browse Files",
                                         command=self.browse_files)
        self.button_explore.pack(side=tk.LEFT, padx=10)

        # Create a button to browse directories
        self.button_browse_dir = ttk.Button(self.button_frame, 
                                            text="Browse Directory",
                                            command=self.browse_directory)
        self.button_browse_dir.pack(side=tk.LEFT, padx=10)

        # Create a button to open the selected file
        self.button_open_file = ttk.Button(self.button_frame, 
                                           text="Open File",
                                           command=self.open_file)
        self.button_open_file.pack(side=tk.LEFT, padx=10)

        # Create a button to exit the application
        self.button_exit = ttk.Button(self.button_frame, 
                                      text="Exit",
                                      command=self.root.destroy)
        self.button_exit.pack(side=tk.LEFT, padx=10)

        # Create a label to display the selected file
        self.label_selected_file = ttk.Label(self.root, 
                                            text="", 
                                            font=("Arial", 12))
        self.label_selected_file.grid(column=1, row=3, padx=10, pady=10)

        # Initialize the selected file path
        self.selected_file_path = ""

    def browse_files(self):
        """Browse files and update the selected file label."""
        self.selected_file_path = filedialog.askopenfilename(initialdir="/",
                                                            title="Select a File",
                                                            filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        self.label_selected_file.config(text="File Opened: " + self.selected_file_path)

    def browse_directory(self):
        """Browse directories and update the selected file label."""
        self.selected_file_path = filedialog.askdirectory(initialdir="/",
                                                          title="Select a Directory")
        self.label_selected_file.config(text="Directory Selected: " + self.selected_file_path)
        
    def open_file(self):
        """Open the selected file and display its content."""
        if self.selected_file_path:
            try:
                if self.selected_file_path.endswith(".txt"):
                    with open(self.selected_file_path, 'r') as file:
                        file_content = file.read()
                        messagebox.showinfo("File Content", file_content)
                else:
                    messagebox.showerror("Error", "Only text files are supported.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a file first.")

    def run(self):
        """Run the application main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    file_explorer = FileExplorer(root)
    file_explorer.run()