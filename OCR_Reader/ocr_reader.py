import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
import os

# If on Windows, uncomment and point to your tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Pro OCR Document Scanner")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2f3640")

        self.image_path = None
        self.extracted_text = ""
        self.setup_ui()

    def setup_ui(self):
        # Left Panel: Image Preview
        self.left_frame = tk.Frame(self.root, bg="#353b48", width=500)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.img_label = tk.Label(self.left_frame, text="Upload an Image to Scan", fg="white", bg="#353b48")
        self.img_label.pack(fill="both", expand=True)

        # Right Panel: Text & Controls
        self.right_frame = tk.Frame(self.root, bg="#2f3640", width=400)
        self.right_frame.pack(side="right", fill="both", padx=10, pady=10)

        tk.Label(self.right_frame, text="Extracted Text", fg="#f5f6fa", bg="#2f3640", font=("Arial", 12, "bold")).pack(pady=5)
        self.text_area = tk.Text(self.right_frame, wrap="word", font=("Consolas", 10))
        self.text_area.pack(fill="both", expand=True, pady=5)

        # Buttons
        btn_config = {"font": ("Arial", 10, "bold"), "fg": "white", "pady": 8}
        tk.Button(self.right_frame, text="📂 Upload Image", command=self.upload_image, bg="#0097e6", **btn_config).pack(fill="x", pady=5)
        tk.Button(self.right_frame, text="🔍 Extract Text", command=self.perform_ocr, bg="#44bd32", **btn_config).pack(fill="x", pady=5)
        tk.Button(self.right_frame, text="📄 Export to PDF", command=self.export_pdf, bg="#e84118", **btn_config).pack(fill="x", pady=5)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            img = Image.open(self.image_path)
            img.thumbnail((450, 600))
            self.photo = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.photo, text="")

    def perform_ocr(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload an image first!")
            return

        # Image Pre-processing for better OCR
        img = cv2.imread(self.image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Thresholding to get a "scanned" look (black and white)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # OCR Extraction
        self.extracted_text = pytesseract.image_to_string(thresh)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, self.extracted_text)

    def export_pdf(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Error", "Nothing to export!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if save_path:
            c = canvas.Canvas(save_path)
            # Simple text-to-PDF logic
            text_object = c.beginText(40, 800)
            text_object.setFont("Helvetica", 10)
            
            for line in text.split('\n'):
                text_object.textLine(line)
            
            c.drawText(text_object)
            c.save()
            messagebox.showinfo("Success", f"PDF saved at {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRScanner(root)
    root.mainloop()