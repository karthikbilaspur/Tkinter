from tkinter import *
from tkinter.ttk import *
from time import strftime
from datetime import date
from tkinter import messagebox

class DigitalClock:
    def __init__(self):
        self.root = Tk()
        self.root.title('Digital Clock')
        self.alarm_set = False

        # Digital Clock
        self.time_label = Label(self.root, font=('calibri', 40, 'bold'),
                         background='purple',
                         foreground='white')
        self.time_label.pack(anchor='center')

        # Date Display
        self.date_label = Label(self.root, font=('calibri', 20, 'bold'),
                              background='purple',
                              foreground='white')
        self.date_label.pack(anchor='center')

        # Alarm Settings
        self.alarm_frame = Frame(self.root)
        self.alarm_frame.pack(anchor='center')
        self.alarm_label = Label(self.alarm_frame, text='Alarm Time (HH:MM:SS):')
        self.alarm_label.pack(side=LEFT)
        self.alarm_entry = Entry(self.alarm_frame, width=10)
        self.alarm_entry.pack(side=LEFT)
        self.alarm_button = Button(self.alarm_frame, text='Set Alarm', command=self.set_alarm)
        self.alarm_button.pack(side=LEFT)

        # Update Time and Date
        self.update_time()

    def update_time(self) -> None:
        """Update the time and date labels."""
        current_time = strftime('%H:%M:%S %p')
        self.time_label.config(text=current_time)
        self.date_label.config(text=str(date.today()))
        if self.alarm_set:
            self.check_alarm()
        self.schedule_next_update()

    def schedule_next_update(self) -> None:
        """Schedule the next update using the after method."""
        self.time_label.after(1000, self.update_time)

    def set_alarm(self) -> None:
        """Set the alarm based on the user input."""
        alarm_time = self.alarm_entry.get()
        if alarm_time:
            try:
                self.alarm_button.config(text='Alarm Set')
                self.alarm_set = True
            except ValueError:
                messagebox.showerror('Error', 'Invalid alarm time format')
        else:
            messagebox.showerror('Error', 'Please enter alarm time')

    def check_alarm(self) -> None:
        """Check if the current time matches the alarm time."""
        alarm_time = self.alarm_entry.get()
        current_time = strftime('%H:%M:%S')
        if current_time == alarm_time:
            messagebox.showinfo('Alarm', 'Wake Up!')
            self.alarm_button.config(text='Set Alarm')
            self.alarm_set = False

    def run(self) -> None:
        """Run the application main loop."""
        self.root.mainloop()

if __name__ == "__main__":
    clock = DigitalClock()
    clock.run()