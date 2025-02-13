import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
import configparser

class RegistrationForm:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.root = tk.Tk()
        self.root.title(self.config['GUI']['title'])
        self.root.geometry(f"{self.config['GUI']['width']}x{self.config['GUI']['height']}")
        self.root.configure(background=self.config['GUI']['background_color'])

        self.create_widgets()

    def create_widgets(self):
        # Create labels
        heading = tk.Label(self.root, text="Registration Form", bg=self.config['GUI']['background_color'])
        heading.grid(row=0, column=1)

        name = tk.Label(self.root, text="Name", bg=self.config['GUI']['background_color'])
        name.grid(row=1, column=0)

        course = tk.Label(self.root, text="Course", bg=self.config['GUI']['background_color'])
        course.grid(row=2, column=0)

        sem = tk.Label(self.root, text="Semester", bg=self.config['GUI']['background_color'])
        sem.grid(row=3, column=0)

        form_no = tk.Label(self.root, text="Form No.", bg=self.config['GUI']['background_color'])
        form_no.grid(row=4, column=0)

        contact_no = tk.Label(self.root, text="Contact No.", bg=self.config['GUI']['background_color'])
        contact_no.grid(row=5, column=0)

        email_id = tk.Label(self.root, text="Email id", bg=self.config['GUI']['background_color'])
        email_id.grid(row=6, column=0)

        address = tk.Label(self.root, text="Address", bg=self.config['GUI']['background_color'])
        address.grid(row=7, column=0)

        # Create entry fields
        self.name_field = tk.Entry(self.root)
        self.name_field.grid(row=1, column=1, ipadx="100")

        self.course_field = tk.Entry(self.root)
        self.course_field.grid(row=2, column=1, ipadx="100")

        self.sem_field = tk.Entry(self.root)
        self.sem_field.grid(row=3, column=1, ipadx="100")

        self.form_no_field = tk.Entry(self.root)
        self.form_no_field.grid(row=4, column=1, ipadx="100")

        self.contact_no_field = tk.Entry(self.root)
        self.contact_no_field.grid(row=5, column=1, ipadx="100")

        self.email_id_field = tk.Entry(self.root)
        self.email_id_field.grid(row=6, column=1, ipadx="100")

        self.address_field = tk.Entry(self.root)
        self.address_field.grid(row=7, column=1, ipadx="100")

        # Create buttons
        submit = tk.Button(self.root, text="Submit", fg="Black", bg="Red", command=self.insert_data)
        submit.grid(row=8, column=1)

        clear = tk.Button(self.root, text="Clear", fg="Black", bg="Red", command=self.clear_fields)
        clear.grid(row=8, column=2)

        # Create a text box to display messages
        self.message_box = tk.Text(self.root, height=5, width=40)
        self.message_box.grid(row=9, column=0, columnspan=3)

    def insert_data(self):
        try:
            # Get data from entry fields
            name = self.name_field.get()
            course = self.course_field.get()
            sem = self.sem_field.get()
            form_no = self.form_no_field.get()
            contact_no = self.contact_no_field.get()
            email_id = self.email_id_field.get()
            address = self.address_field.get()

            # Validate input data
            if not name or not course or not sem or not form_no or not contact_no or not email_id or not address:
                self.message_box.insert(tk.END, "Please fill all fields!\n")
                return

            # Save data to Excel file
            wb = load_workbook(self.config['Excel']['file_path'])
            sheet = wb.active
            sheet.append([name, course, sem, form_no, contact_no, email_id, address])
            wb.save(self.config['Excel']['file_path'])
            self.message_box.insert(tk.END, "Data saved successfully!\n")
        except Exception as e:
            self.message_box.insert(tk.END, f"An error occurred: {str(e)}\n")

    def clear_fields(self):
        # Clear entry fields
        self.name_field.delete(0, tk.END)
        self.course_field.delete(0, tk.END)
        self.sem_field.delete(0, tk.END)
        self.form_no_field.delete(0, tk.END)
        self.contact_no_field.delete(0, tk.END)
        self.email_id_field.delete(0, tk.END)
        self.address_field.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RegistrationForm()
    app.run()