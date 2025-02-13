"""
Weight Converter Application

This application allows users to convert weights between different units.
"""


from tkinter import *
from tkinter import messagebox


class WeightConverter:
    """
    Weight Converter Class

    This class represents the weight converter application.
    It contains methods for converting weights between different units.
    """

    def __init__(self):
        """
        Initializes the Weight Converter Application

        Creates the GUI window and widgets.
        """
        self.window = Tk()
        self.window.title("Weight Converter")

        # Create the Label widgets
        self.e1 = Label(self.window, text="Enter the weight in Kg")
        self.e2_value = StringVar()
        self.e2 = Entry(self.window, textvariable=self.e2_value)
        self.e3 = Label(self.window, text='Gram')
        self.e4 = Label(self.window, text='Pounds')
        self.e5 = Label(self.window, text='Ounce')
        self.e6 = Label(self.window, text='Milligrams')
        self.e7 = Label(self.window, text='Micrograms')

        # Create the Text Widgets
        self.t1 = Text(self.window, height=1, width=20)
        self.t2 = Text(self.window, height=1, width=20)
        self.t3 = Text(self.window, height=1, width=20)
        self.t4 = Text(self.window, height=1, width=20)
        self.t5 = Text(self.window, height=1, width=20)

        # Create the Button Widget
        self.b1 = Button(self.window, text="Convert", command=self.from_kg)

        # grid method is used for placing 
        # the widgets at respective positions 
        # in table like structure
        self.e1.grid(row=0, column=0)
        self.e2.grid(row=0, column=1)
        self.e3.grid(row=1, column=0)
        self.e4.grid(row=1, column=1)
        self.e5.grid(row=1, column=2)
        self.e6.grid(row=2, column=0)
        self.e7.grid(row=2, column=1)
        self.t1.grid(row=3, column=0)
        self.t2.grid(row=3, column=1)
        self.t3.grid(row=3, column=2)
        self.t4.grid(row=4, column=0)
        self.t5.grid(row=4, column=1)
        self.b1.grid(row=0, column=2)

    def from_kg(self):
        """
        Converts Weight from Kilograms to Other Units

        Converts the weight from kilograms to grams, pounds, ounces, milligrams, and micrograms.
        """
        try:
            # Get the weight in kilograms
            kg = float(self.e2_value.get())

            # Validate for negative input
            if kg < 0:
                self.t1.delete("1.0", END)
                self.t1.insert(END, "Invalid input")
                
                self.t2.delete("1.0", END)
                self.t2.insert(END, "Invalid input")
                
                self.t3.delete("1.0", END)
                self.t3.insert(END, "Invalid input")
                
                self.t4.delete("1.0", END)
                self.t4.insert(END, "Invalid input")
                
                self.t5.delete("1.0", END)
                self.t5.insert(END, "Invalid input")
                return

            # Convert kg to gram
            gram = kg * 1000
            
            # Convert kg to pound
            pound = kg * 2.20462
            
            # Convert kg to ounce
            ounce = kg * 35.274
            
            # Convert kg to milligram
            milligram = kg * 1000000
            
            # Convert kg to microgram
            microgram = kg * 1000000000
            
            # Enters the converted weight to 
            # the text widget
            self.t1.delete("1.0", END)
            self.t1.insert(END, f"{gram:.2f} g")
            
            self.t2.delete("1.0", END)
            self.t2.insert(END, f"{pound:.2f} lb")
            
            self.t3.delete("1.0", END)
            self.t3.insert(END, f"{ounce:.2f} oz")
            
            self.t4.delete("1.0", END)
            self.t4.insert(END, f"{milligram:.2f} mg")
            
            self.t5.delete("1.0", END)
            self.t5.insert(END, f"{microgram:.2f} mcg")
        except ValueError:
            self.t1.delete("1.0", END)
            self.t1.insert(END, "Invalid input")
            
            self.t2.delete("1.0", END)
            self.t2.insert(END, "Invalid input")
            
            self.t3.delete("1.0", END)
            self.t3.insert(END, "Invalid input")
            
            self.t4.delete("1.0", END)
            self.t4.insert(END, "Invalid input")
            
            self.t5.delete("1.0", END)
            self.t5.insert(END, "Invalid input")

    def run(self):
        """
        Runs the Weight Converter Application

        Starts the main event loop of the application.
        """
        self.window.mainloop()


if __name__ == "__main__":
    converter = WeightConverter()
    converter.run()