from tkinter import *
import calendar

# Constants
WIDTH = 550
HEIGHT = 600
SMALL_WIDTH = 250
SMALL_HEIGHT = 140
TITLE_FONT_SIZE = 28
CALENDAR_FONT_SIZE = 10
CALENDAR_FONT = "Consolas"
TITLE_FONT = "times"
BACKGROUND_COLOR = "white"
DARK_GRAY = "dark gray"
LIGHT_GREEN = "light green"
RED = "red"
BLACK = "black"

class CalendarApp:
    def __init__(self, root):
        """
        Initialize the CalendarApp.
        
        Args:
        root (Tk): The root window.
        """
        self.root = root
        self.root.config(background=BACKGROUND_COLOR)
        self.root.title("CALENDAR")
        self.root.geometry(f"{SMALL_WIDTH}x{SMALL_HEIGHT}")

        self.create_widgets()

    def create_widgets(self):
        """
        Create the widgets for the main window.
        """
        # Create a CALENDAR : label with specified font and size
        self.cal_label = Label(self.root, text="CALENDAR", bg=DARK_GRAY, font=(TITLE_FONT, TITLE_FONT_SIZE, 'bold'))
        self.cal_label.grid(row=1, column=1)

        # Create a Enter Year : label
        self.year_label = Label(self.root, text="Enter Year", bg=LIGHT_GREEN)
        self.year_label.grid(row=2, column=1)

        # Create a text entry box for filling or typing the information.
        self.year_field = Entry(self.root)
        self.year_field.grid(row=3, column=1)

        # Create a Show Calendar Button and attached to showCal function
        self.show_button = Button(self.root, text="Show Calendar", fg=BLACK, bg=RED, command=self.show_cal)
        self.show_button.grid(row=4, column=1)

        # Create a Exit Button and attached to exit function
        self.exit_button = Button(self.root, text="Exit", fg=BLACK, bg=RED, command=self.root.destroy)
        self.exit_button.grid(row=6, column=1)

    def show_cal(self):
        """
        Show the calendar for the given year.
        """
        try:
            year = int(self.year_field.get())
            if year < 1:
                raise ValueError
            self.create_calendar_window(year)
        except ValueError:
            messagebox.showerror("Invalid Year", "Please enter a valid year.")

    def create_calendar_window(self, year):
        """
        Create a new window to display the calendar.
        
        Args:
        year (int): The year to display.
        """
        # Create a GUI window
        cal_window = Toplevel(self.root)
        cal_window.config(background=BACKGROUND_COLOR)
        cal_window.title("CALENDAR")
        cal_window.geometry(f"{WIDTH}x{HEIGHT}")

        # Create a label for showing the content of the calendar
        cal_content = calendar.calendar(year)
        cal_year = Label(cal_window, text=cal_content, font=(CALENDAR_FONT, CALENDAR_FONT_SIZE, "bold"), justify=LEFT)
        cal_year.grid(row=5, column=1, padx=20)

        cal_window.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = CalendarApp(root)
    root.mainloop()