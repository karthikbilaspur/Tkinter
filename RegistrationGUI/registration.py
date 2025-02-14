import tkinter as tk
from tkinter import messagebox, simpledialog
from openpyxl import load_workbook
import configparser
import hashlib
import logging
import os

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

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

        login = tk.Button(self.root, text="Login", fg="Black", bg="Red", command=self.login)
        login.grid(row=8, column=3)

        # Create a text box to display messages
        self.message_box = tk.Text(self.root, height=5, width=40)
        self.message_box.grid(row=9, column=0, columnspan=4)

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

            # Hash sensitive data
            contact_no_hash = hashlib.sha256(contact_no.encode()).hexdigest()
            email_id_hash = hashlib.sha256(email_id.encode()).hexdigest()

            # Save data to Excel file
            wb = load_workbook(self.config['Excel']['file_path'])
            sheet = wb.active
            sheet.append([name, course, sem, form_no, contact_no_hash, email_id_hash, address])
            wb.save(self.config['Excel']['file_path'])
                        self.message_box.insert(tk.END, "Data saved successfully!\n")
            logging.info("Data saved successfully!")
        except Exception as e:
            self.message_box.insert(tk.END, f"An error occurred: {str(e)}\n")
            logging.error(f"An error occurred: {str(e)}")

    def clear_fields(self):
        # Clear entry fields
        self.name_field.delete(0, tk.END)
        self.course_field.delete(0, tk.END)
        self.sem_field.delete(0, tk.END)
        self.form_no_field.delete(0, tk.END)
        self.contact_no_field.delete(0, tk.END)
        self.email_id_field.delete(0, tk.END)
        self.address_field.delete(0, tk.END)

    def login(self):
        # Create a new window for login
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")

        # Create labels and entry fields
        username_label = tk.Label(self.login_window, text="Username")
        username_label.grid(row=0, column=0)
        self.username_field = tk.Entry(self.login_window)
        self.username_field.grid(row=0, column=1)

        password_label = tk.Label(self.login_window, text="Password")
        password_label.grid(row=1, column=0)
        self.password_field = tk.Entry(self.login_window, show="*")
        self.password_field.grid(row=1, column=1)

        # Create a button to submit the login credentials
        submit_button = tk.Button(self.login_window, text="Submit", command=self.check_credentials)
        submit_button.grid(row=2, column=1)

    def check_credentials(self):
        # Get the username and password from the entry fields
        username = self.username_field.get()
        password = self.password_field.get()

        # Hash the password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username and password match the stored credentials
        if username == self.config['Credentials']['username'] and password_hash == self.config['Credentials']['password_hash']:
            self.message_box.insert(tk.END, "Login successful!\n")
            logging.info("Login successful!")
        else:
            self.message_box.insert(tk.END, "Invalid username or password!\n")
            logging.error("Invalid username or password!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RegistrationForm()
    app.run()