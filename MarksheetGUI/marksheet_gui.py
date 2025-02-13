import tkinter as tk

class Marksheet:
    def __init__(self, root):
        self.root = root
        self.root.title("MARKSHEET")
        self.root.geometry("700x250")

        # Define constants
        self.SUBJECT_CREDITS = {
            "CS 201": 4,
            "CS 202": 4,
            "MA 201": 3,
            "EC 201": 4
        }
        self.GRADE_CREDITS = {
            "A": 10,
            "B": 9,
            "C": 8,
            "D": 7,
            "P": 6,
            "F": 0
        }

        # Create GUI elements
        self.name_label = tk.Label(root, text="Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        self.reg_label = tk.Label(root, text="Reg.No")
        self.reg_label.grid(row=0, column=3)
        self.reg_entry = tk.Entry(root)
        self.reg_entry.grid(row=0, column=4)

        self.roll_label = tk.Label(root, text="Roll.No")
        self.roll_label.grid(row=1, column=0)
        self.roll_entry = tk.Entry(root)
        self.roll_entry.grid(row=1, column=1)

        self.subjects = []
        self.grades = []
        for i, (subject, credit) in enumerate(self.SUBJECT_CREDITS.items()):
            subject_frame = tk.Frame(root)
            subject_frame.grid(row=i+2, column=0, columnspan=5)

            subject_label = tk.Label(subject_frame, text=subject)
            subject_label.pack(side=tk.LEFT)

            grade_label = tk.Label(subject_frame, text="Grade")
            grade_label.pack(side=tk.LEFT)

            grade_entry = tk.Entry(subject_frame)
            grade_entry.pack(side=tk.LEFT)

            credit_label = tk.Label(subject_frame, text=str(credit))
            credit_label.pack(side=tk.LEFT)

            self.subjects.append(subject_label)
            self.grades.append(grade_entry)

        self.total_credit_label = tk.Label(root, text="Total credit")
        self.total_credit_label.grid(row=len(self.SUBJECT_CREDITS)+2, column=3)
        self.total_credit_value = tk.Label(root, text="")
        self.total_credit_value.grid(row=len(self.SUBJECT_CREDITS)+2, column=4)

        self.sgpa_label = tk.Label(root, text="SGPA")
        self.sgpa_label.grid(row=len(self.SUBJECT_CREDITS)+3, column=3)
        self.sgpa_value = tk.Label(root, text="")
        self.sgpa_value.grid(row=len(self.SUBJECT_CREDITS)+3, column=4)

        self.submit_button = tk.Button(root, text="Submit", command=self.calculate)
        self.submit_button.grid(row=len(self.SUBJECT_CREDITS)+3, column=1)

    def calculate(self):
        total_credits = 0
        for grade_entry in self.grades:
            grade = grade_entry.get()
            if grade in self.GRADE_CREDITS:
                subject_index = self.grades.index(grade_entry)
                subject_credit = self.SUBJECT_CREDITS[self.subjects[subject_index].cget("text")]
                total_credits += self.GRADE_CREDITS[grade] * subject_credit
            else:
                print("Invalid grade")
        self.total_credit_value.config(text=str(total_credits))
        self.sgpa_value.config(text=str(total_credits / sum(self.SUBJECT_CREDITS.values())))

if __name__ == "__main__":
    root = tk.Tk()
    marksheet = Marksheet(root)
    root.mainloop()