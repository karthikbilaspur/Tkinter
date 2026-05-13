import tkinter as tk
from tkinter import font
from pygments import lexers, highlight
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

class MiniVSCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini VS Code")
        self.root.geometry("900x600")
        
        # Theme Colors (Monokai-ish)
        self.bg_color = "#272822"
        self.fg_color = "#f8f8f2"
        self.line_num_bg = "#23241f"
        self.line_num_fg = "#8f908a"

        self.setup_ui()

    def setup_ui(self):
        # Main Container
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)

        # Line Numbers Canvas
        self.line_numbers = tk.Canvas(self.container, width=50, bg=self.line_num_bg, highlightthickness=0)
        self.line_numbers.pack(side="left", fill="y")

        # Text Editor
        self.editor = tk.Text(
            self.container, 
            bg=self.bg_color, 
            fg=self.fg_color,
            insertbackground="white", # Cursor color
            font=("Consolas", 12),
            undo=True,
            borderwidth=0,
            padx=10,
            wrap="none"
        )
        self.editor.pack(side="right", fill="both", expand=True)

        # Binding events for real-time updates
        self.editor.bind("<<Modified>>", self.on_content_changed)
        self.editor.bind("<KeyRelease>", self.update_line_numbers)
        self.editor.bind("<MouseWheel>", self.update_line_numbers)

        # Setup Highlight Tags based on Pygments
        self.setup_tags()

    def setup_tags(self):
        # Define a few basic tags for syntax highlighting
        self.editor.tag_configure("Keyword", fg="#f92672")
        self.editor.tag_configure("Name.Function", fg="#a6e22e")
        self.editor.tag_configure("String", fg="#e6db74")
        self.editor.tag_configure("Comment", fg="#75715e")
        self.editor.tag_configure("Number", fg="#ae81ff")

    def update_line_numbers(self, event=None):
        self.line_numbers.delete("all")
        i = self.editor.index("@0,0")
        while True:
            dline = self.editor.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.line_numbers.create_text(
                25, y, text=linenum, anchor="n", 
                fill=self.line_num_fg, font=("Consolas", 11)
            )
            i = self.editor.index(f"{i}+1line")

    def apply_highlighting(self):
        code = self.editor.get("1.0", tk.END)
        self.editor.mark_set("range_start", "1.0")
        
        # Clear existing tags
        for tag in ["Keyword", "Name.Function", "String", "Comment", "Number"]:
            self.editor.tag_remove(tag, "1.0", tk.END)

        # Use Pygments to lex the code
        lexer = PythonLexer()
        for token_type, value in lexer.get_tokens(code):
            token_str = str(token_type)
            
            # Simple mapping Pygments types to our tags
            tag_name = None
            if "Keyword" in token_str: tag_name = "Keyword"
            elif "Function" in token_str: tag_name = "Name.Function"
            elif "String" in token_str: tag_name = "String"
            elif "Comment" in token_str: tag_name = "Comment"
            elif "Number" in token_str: tag_name = "Number"

            if tag_name:
                start = self.editor.index("range_start")
                end = self.editor.index(f"range_start + {len(value)} chars")
                self.editor.tag_add(tag_name, start, end)
            
            self.editor.mark_set("range_start", f"range_start + {len(value)} chars")

    def on_content_changed(self, event=None):
        if self.editor.edit_modified():
            self.apply_highlighting()
            self.update_line_numbers()
            self.editor.edit_modified(False) # Reset modified flag

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniVSCode(root)
    root.mainloop()