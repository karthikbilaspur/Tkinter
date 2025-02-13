import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from tkinter import Tk, Label, Button, Entry, StringVar

class LoanCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Loan Calculator')
        self.setGeometry(300, 300, 300, 200)

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Annual Interest Rate'), 0, 0)
        self.annualInterestRateEdit = QLineEdit()
        layout.addWidget(self.annualInterestRateEdit, 0, 1)

        layout.addWidget(QLabel('Number of Years'), 1, 0)
        self.numberOfYearsEdit = QLineEdit()
        layout.addWidget(self.numberOfYearsEdit, 1, 1)

        layout.addWidget(QLabel('Loan Amount'), 2, 0)
        self.loanAmountEdit = QLineEdit()
        layout.addWidget(self.loanAmountEdit, 2, 1)

        layout.addWidget(QLabel('Monthly Payment'), 3, 0)
        self.monthlyPaymentLabel = QLabel()
        layout.addWidget(self.monthlyPaymentLabel, 3, 1)

        layout.addWidget(QLabel('Total Payment'), 4, 0)
        self.totalPaymentLabel = QLabel()
        layout.addWidget(self.totalPaymentLabel, 4, 1)

        buttonLayout = QVBoxLayout()
        layout.addLayout(buttonLayout, 5, 0, 1, 2)

        computeButton = QPushButton('Compute Payment')
        computeButton.clicked.connect(self.computePayment)
        buttonLayout.addWidget(computeButton)

        self.show()

    def computePayment(self):
        try:
            monthlyPayment = self.getMonthlyPayment(
                float(self.loanAmountEdit.text()),
                float(self.annualInterestRateEdit.text()) / 1200,
                int(self.numberOfYearsEdit.text())
            )

            self.monthlyPaymentLabel.setText(f'{monthlyPayment:.2f}')
            totalPayment = float(self.monthlyPaymentLabel.text()) * 12 * int(self.numberOfYearsEdit.text())
            self.totalPaymentLabel.setText(f'{totalPayment:.2f}')
        except ValueError:
            self.monthlyPaymentLabel.setText('Invalid input')
            self.totalPaymentLabel.setText('')

    def getMonthlyPayment(self, loanAmount, monthlyInterestRate, numberOfYears):
        monthlyPayment = loanAmount * monthlyInterestRate / (1 - 1 / (1 + monthlyInterestRate) ** (numberOfYears * 12))
        return monthlyPayment


def main():
    app = QApplication(sys.argv)
    ex = LoanCalculator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# Tkinter GUI
def calculate_payment():
    try:
        loan_amount = float(loan_amount_entry.get())
        annual_interest_rate = float(annual_interest_rate_entry.get()) / 1200
        number_of_years = int(number_of_years_entry.get())

        monthly_payment = loan_amount * annual_interest_rate / (1 - 1 / (1 + annual_interest_rate) ** (number_of_years * 12))
        total_payment = monthly_payment * 12 * number_of_years

        monthly_payment_label.config(text=f'Monthly Payment: {monthly_payment:.2f}')
        total_payment_label.config(text=f'Total Payment: {total_payment:.2f}')
    except ValueError:
        monthly_payment_label.config(text='Invalid input')
        total_payment_label.config(text='')

root = Tk()
root.title('Loan Calculator')

loan_amount_label = Label(root, text='Loan Amount')
loan_amount_label.grid(row=0, column=0)
loan_amount_entry = Entry(root)
loan_amount_entry.grid(row=0, column=1)

annual_interest_rate_label = Label(root, text='Annual Interest Rate')
annual_interest_rate_label.grid(row=1, column=0)
annual_interest_rate_entry = Entry(root)
annual_interest_rate_entry.grid(row=1, column=1)

number_of_years_label = Label(root, text='Number of Years')
number_of_years_label.grid(row=2, column=0)
number_of_years_entry = Entry(root)
number_of_years_entry.grid(row=2, column=1)

calculate_button = Button(root, text='Calculate Payment', command=calculate_payment)
calculate_button.grid(row=3, column=0, columnspan=2)

monthly_payment_label = Label(root, text='Monthly Payment')
monthly_payment_label.grid(row=4, column=0, columnspan=2)

total_payment_label = Label(root, text='Total Payment')
total_payment_label.grid(row=5, column=0, columnspan=2)

root.mainloop()
