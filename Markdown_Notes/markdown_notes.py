import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import markdown2
import json

class MarkdownNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("Lumina Markdown Editor")
        self.root.geometry("1100x700")
        
        # Theme Configurations
        self.themes = {
            "Dark": {"bg": "#1e1e1e", "fg": "#d4d4d4", "accent": "#37373d", "preview_bg": "#252526"},
            "Nord": {"bg": "#2e3440", "fg": "#d8dee9", "accent": "#434c5e", "preview_bg": "#3b4252"},
            "Solarized": {"bg": "#002b36", "fg": "#839496", "accent": "#073642", "preview_bg": "#073642"}
        }
        self.current_theme = "Dark"
        
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # Toolbar
        self.toolbar = tk.Frame(self.root, bg="#333", height=40)
        self.toolbar.pack(side="top", fill="x")

        # Theme Dropdown
        self.theme_var = tk.StringVar(value="Dark")
        theme_menu = ttk.Combobox(self.toolbar, textvariable=self.theme_var, values=list(self.themes.keys()), width=10)
        theme_menu.pack(side="left", padx=10, pady=5)
        theme_menu.bind("<<ComboboxSelected>>", self.change_theme)

        tk.Button(self.toolbar, text="💾 Export PDF/HTML", command=self.export_note, bg="#444", fg="white").pack(side="right", padx=10)
        tk.Button(self.toolbar, text="📂 Open", command=self.open_file, bg="#444", fg="white").pack(side="right")

        # Main Paned Window
        self.paned = tk.PanedWindow(self.root, orient="horizontal", sashwidth=4, bg="#333")
        self.paned.pack(fill="both", expand=True)

        # Editor (Left)
        self.editor = tk.Text(self.paned, font=("Consolas", 12), undo=True, borderwidth=0, padx=15, pady=15)
        self.paned.add(self.editor)
        self.editor.bind("<KeyRelease>", self.update_preview)

        # Preview (Right)
        # Note: We use a standard Text widget with tagging for a "lightweight" preview.
        self.preview = tk.Text(self.paned, font=("Arial", 12), state="disabled", borderwidth=0, padx=15, pady=15)
        self.paned.add(self.preview)

    def update_preview(self, event=None):
        content = self.editor.get("1.0", tk.END)
        # Convert Markdown to HTML (Internal representation)
        html_content = markdown2.markdown(content)
        
        # Simple rendering logic for the preview pane
        self.preview.config(state="normal")
        self.preview.delete("1.0", tk.END)
        self.preview.insert("1.0", content) # For true HTML rendering, consider 'tkinterweb'
        self.format_preview_text()
        self.preview.config(state="disabled")

    def format_preview_text(self):
        """Basic Regex-based visual formatting for the live preview."""
        self.preview.tag_remove("h1", "1.0", tk.END)
        
        # Formatting Headers
        content = self.preview.get("1.0", tk.END).split('\n')
        for i, line in enumerate(content):
            if line.startswith("# "):
                self.preview.tag_add("h1", f"{i+1}.0", f"{i+1}.end")
        
        self.preview.tag_config("h1", font=("Arial", 18, "bold"), foreground="#89b4fa")

    def apply_theme(self):
        t = self.themes[self.current_theme]
        self.editor.configure(bg=t["bg"], fg=t["fg"], insertbackground="white")
        self.preview.configure(bg=t["preview_bg"], fg=t["fg"])
        self.toolbar.configure(bg=t["accent"])

    def change_theme(self, event):
        self.current_theme = self.theme_var.get()
        self.apply_theme()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Markdown", "*.md"), ("Text", "*.txt")])
        if path:
            with open(path, 'r') as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())
            self.update_preview()

    def export_note(self):
        path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML File", "*.html")])
        if path:
            content = self.editor.get("1.0", tk.END)
            html = markdown2.markdown(content)
            # Wrap in basic HTML boilerplate
            full_html = f"<html><body style='font-family:sans-serif; padding:40px;'>{html}</body></html>"
            with open(path, 'w') as f:
                f.write(full_html)
            messagebox.showinfo("Exported", "Document exported as HTML successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownNotes(root)
    root.mainloop()