"""
Visiting Card Scanner Application

This application allows users to upload an image of a visiting card,
scan the image using OCR, and display the extracted text.

Author: [V.Karthik]
Date: [10/10/2024]
"""


import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import os


class VisitingCardScanner:
    """
    Visiting Card Scanner Class

    This class represents the visiting card scanner application.
    It contains methods for uploading an image, scanning the image,
    and displaying the extracted text.
    """

    def __init__(self, root):
        """
        Initializes the Visiting Card Scanner Application

        Args:
            root (tkinter.Tk): The root window of the application
        """
        self.root = root
        self.root.title("Visiting Card Scanner")
        self.root.geometry("800x500")
        self.root.maxsize(1000, 500)
        self.root.minsize(600, 500)

        self.create_menu_bar()
        self.create_widgets()

    def create_menu_bar(self):
        """
        Creates the Menu Bar for the Application

        The menu bar contains options for uploading an image and exiting the application.
        """
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Image", command=self.upload_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def create_widgets(self):
        """
        Creates the Widgets for the Application

        The widgets include a header label, an upload button, a status label,
        a text area, and a convert button.
        """
        header_label = tk.Label(self.root, text="Visiting Card Scanner", bg="#FAD2B8", fg="#39322D", font=("Times", 18))
        header_label.pack(fill="x")

        upload_frame = tk.Frame(self.root)
        upload_frame.pack(side="top", fill="x", padx=10, pady=10)

        upload_button = tk.Button(upload_frame, text="Upload Card", bg="#F58D4B", font=("Times", 15), command=self.upload_file)
        upload_button.pack(side="left", padx=5, pady=5)

        self.status_label = tk.Label(self.root, text="Please upload an image to scan", bg="white", fg="red")
        self.status_label.pack()

        self.text_area = tk.Text(self.root, height=9, font=("Times", 13))
        self.text_area.pack(side="bottom", fill="x")

        convert_button = tk.Button(self.root, text="Scan and Convert", bg="#F58D4B", font=("Times", 15), command=self.convert)
        convert_button.pack(side="bottom", pady="10")

        self.filename = None
        self.uploaded_image_label = None

    def upload_file(self):
        """
        Uploads an Image File

        Opens a file dialog for the user to select an image file.
        Updates the status label and displays the uploaded image.
        """
        self.filename = filedialog.askopenfilename(initialdir="/Desktop", title="Select a card image", filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        if self.filename:
            self.status_label.config(text="Image uploaded successfully", fg="#0CDD19")
            self.display_uploaded_image()

    def display_uploaded_image(self):
        """
        Displays the Uploaded Image

        Destroys any previously uploaded image and displays the new image.
        """
        if self.uploaded_image_label:
            self.uploaded_image_label.destroy()

        img = Image.open(self.filename)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        self.uploaded_image_label = tk.Label(self.root, image=photo)
        self.uploaded_image_label.image = photo
        self.uploaded_image_label.pack()

    def convert(self):
        """
        Scans the Uploaded Image and Extracts Text

        Uses OCR to scan the uploaded image and extracts the text.
        Displays the extracted text in the text area.
        """
        if self.filename:
            try:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
                text = pytesseract.image_to_string(self.filename)
                self.text_area.delete(1.0, "end")
                self.text_area.insert("end", text)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please upload an image to scan")


if __name__ == "__main__":
    root = tk.Tk()
    app = VisitingCardScanner(root)
    root.mainloop()