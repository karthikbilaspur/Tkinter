from tkinter import Tk, Button, Entry, StringVar

# Constants
BACKGROUND_COLOR = "light green"
BUTTON_BACKGROUND_COLOR = "red"
BUTTON_FOREGROUND_COLOR = "black"

# Function to update expression in the text entry box
def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

# Function to evaluate the final expression
def equalpress():
    try:
        global expression
        total = str(eval(expression))
        equation.set(total)
        expression = ""
    except:
        equation.set("error")
        expression = ""

# Function to clear the contents of text entry box
def clear():
    global expression
    expression = ""
    equation.set("")

# Driver code
if __name__ == "__main__":
    gui = Tk()
    gui.configure(background=BACKGROUND_COLOR)
    gui.title("Simple Calculator")
    gui.geometry("270x200")

    expression = ""
    equation = StringVar()

    expression_field = Entry(gui, textvariable=equation)
    expression_field.grid(columnspan=4, ipadx=70)

    Button(gui, text='1', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(1), height=1, width=7).grid(row=1, column=0)
    Button(gui, text='2', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(2), height=1, width=7).grid(row=1, column=1)
    Button(gui, text='3', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(3), height=1, width=7).grid(row=1, column=2)
    Button(gui, text='4', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(4), height=1, width=7).grid(row=2, column=0)
    Button(gui, text='5', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(5), height=1, width=7).grid(row=2, column=1)
    Button(gui, text='6', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(6), height=1, width=7).grid(row=2, column=2)
    Button(gui, text='7', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(7), height=1, width=7).grid(row=3, column=0)
    Button(gui, text='8', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(8), height=1, width=7).grid(row=3, column=1)
    Button(gui, text='9', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(9), height=1, width=7).grid(row=3, column=2)
    Button(gui, text='0', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press(0), height=1, width=7).grid(row=4, column=0)

    Button(gui, text='+', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press("+"), height=1, width=7).grid(row=1, column=3)
    Button(gui, text='-', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press("-"), height=1, width=7).grid(row=2, column=3)
    Button(gui, text='*', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press("*"), height=1, width=7).grid(row=3, column=3)
    Button(gui, text='/', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           
           command=lambda: press("/"), height=1, width=7).grid(row=4, column=3)

    Button(gui, text='=', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=equalpress, height=1, width=7).grid(row=4, column=2)
    Button(gui, text='Clear', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=clear, height=1, width=7).grid(row=4, column=1)
    Button(gui, text='.', bg=BUTTON_BACKGROUND_COLOR, fg=BUTTON_FOREGROUND_COLOR,
           command=lambda: press('.'), height=1, width=7).grid(row=5, column=0)

    gui.mainloop()
    
    