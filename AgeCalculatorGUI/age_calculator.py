from tkinter import *
from tkinter import messagebox
from datetime import date

class AgeCalculator:
    def __init__(self):
        self.gui = Tk()
        self.gui.configure(background="light green")
        self.gui.title("Age Calculator")
        self.gui.geometry("525x350")

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        dob = Label(self.gui, text="Date Of Birth", bg="blue")
        dob.grid(row=0, column=1)

        day = Label(self.gui, text="Day", bg="light green")
        day.grid(row=1, column=0)
        self.dayField = Entry(self.gui)
        self.dayField.grid(row=1, column=1)

        month = Label(self.gui, text="Month", bg="light green")
        month.grid(row=2, column=0)
        self.monthField = Entry(self.gui)
        self.monthField.grid(row=2, column=1)

        year = Label(self.gui, text="Year", bg="light green")
        year.grid(row=3, column=0)
        self.yearField = Entry(self.gui)
        self.yearField.grid(row=3, column=1)

        givenDate = Label(self.gui, text="Given Date", bg="blue")
        givenDate.grid(row=0, column=4)

        givenDay = Label(self.gui, text="Given Day", bg="light green")
        givenDay.grid(row=1, column=3)
        self.givenDayField = Entry(self.gui)
        self.givenDayField.grid(row=1, column=4)

        givenMonth = Label(self.gui, text="Given Month", bg="light green")
        givenMonth.grid(row=2, column=3)
        self.givenMonthField = Entry(self.gui)
        self.givenMonthField.grid(row=2, column=4)

        givenYear = Label(self.gui, text="Given Year", bg="light green")
        givenYear.grid(row=3, column=3)
        self.givenYearField = Entry(self.gui)
        self.givenYearField.grid(row=3, column=4)

        resultantAge = Button(self.gui, text="Resultant Age", fg="Black", bg="Red", command=self.calculate_age)
        resultantAge.grid(row=4, column=2)

        resultantAgeToday = Button(self.gui, text="Resultant Age Today", fg="Black", bg="Red", command=self.calculate_age_today)
        resultantAgeToday.grid(row=5, column=2)

        clearAllEntry = Button(self.gui, text="Clear All", fg="Black", bg="Red", command=self.clear_all)
        clearAllEntry.grid(row=12, column=2)

        rsltYear = Label(self.gui, text="Years", bg="light green")
        rsltYear.grid(row=6, column=2)
        self.rsltYearField = Entry(self.gui)
        self.rsltYearField.grid(row=7, column=2)

        rsltMonth = Label(self.gui, text="Months", bg="light green")
        rsltMonth.grid(row=8, column=2)
        self.rsltMonthField = Entry(self.gui)
        self.rsltMonthField.grid(row=9, column=2)

        rsltDay = Label(self.gui, text="Days", bg="light green")
        rsltDay.grid(row=10, column=2)
        self.rsltDayField = Entry(self.gui)
        self.rsltDayField.grid(row=11, column=2)

    def clear_all(self):
        """Clears all entry fields."""
        self.dayField.delete(0, END)
        self.monthField.delete(0, END)
        self.yearField.delete(0, END)
        self.givenDayField.delete(0, END)
        self.givenMonthField.delete(0, END)
        self.givenYearField.delete(0, END)
        self.rsltDayField.delete(0, END)
        self.rsltMonthField.delete(0, END)
        self.rsltYearField.delete(0, END)

    def check_error(self):
        """Checks for empty entry fields."""
        if (self.dayField.get() == "" or self.monthField.get() == ""
            or self.yearField.get() == "" or self.givenDayField.get() == ""
            or self.givenMonthField.get() == "" or self.givenYearField.get() == ""):
            messagebox.showerror("Input Error")
            self.clear_all()
            return -1
        return 0

    def calculate_age(self):
        """Calculates age based on given dates."""
        value = self.check_error()
        if value == -1:
            return

        birth_day = int(self.dayField.get())
        birth_month = int(self.monthField.get())
        birth_year = int(self.yearField.get())

        given_day = int(self.givenDayField.get())
        given_month = int(self.givenMonthField.get())
        given_year = int(self.givenYearField.get())

        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if birth_day > given_day:
            given_month -= 1
            given_day += months[birth_month-1]

        if birth_month > given_month:
            given_year -= 1
            given_month += 12

        calculated_day = given_day - birth_day
        calculated_month = given_month - birth_month
        calculated_year = given_year - birth_year

        self.rsltDayField.insert(10, str(calculated_day))
        self.rsltMonthField.insert(10, str(calculated_month))
        self.rsltYearField.insert(10, str(calculated_year))

    def calculate_age_today(self):
        """Calculates age based on current date."""
        value = self.check_error()
        if value == -1:
            return

        birth_day = int(self.dayField.get())
        birth_month = int(self.monthField.get())
        birth_year = int(self.yearField.get())

        today = date.today()
        given_day = today.day
        given_month = today.month
        given_year = today.year

        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if birth_day > given_day:
            given_month -= 1
            given_day += months[birth_month-1]

        if birth_month > given_month:
            given_year -= 1
            given_month += 12

        calculated_day = given_day - birth_day
        calculated_month = given_month - birth_month
        calculated_year = given_year - birth_year

        self.rsltDayField.insert(10, str(calculated_day))
        self.rsltMonthField.insert(10, str(calculated_month))
        self.rsltYearField.insert(10, str(calculated_year))

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    calculator = AgeCalculator()
    calculator.run()