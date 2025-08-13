import requests
import re
from tkinter import *
import tkinter as tk
from tkinter import ttk

# Country + Currency mapping
country_currency_map = {
    "🇺🇸 United States (USD)": "USD",
    "🇮🇳 India (INR)": "INR",
    "🇯🇵 Japan (JPY)": "JPY",
    "🇬🇧 United Kingdom (GBP)": "GBP",
    "🇪🇺 Eurozone (EUR)": "EUR",
    "🇨🇳 China (CNY)": "CNY",
    "🇨🇦 Canada (CAD)": "CAD",
    "🇦🇺 Australia (AUD)": "AUD",
    "🇨🇭 Switzerland (CHF)": "CHF",
    "🇸🇬 Singapore (SGD)": "SGD"
}

class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        if from_currency != 'USD': 
            amount = amount / self.currencies[from_currency] 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class App(tk.Tk):

    def __init__(self, converter):
        super().__init__()
        self.title = 'Currency Converter'
        self.currency_converter = converter
        self.geometry("520x260")
        self.resizable(False, False)  # Prevent window resize

        # Label
        self.intro_label = Label(self, text='Welcome to Real Time Currency Converter', fg='blue', relief=tk.RAISED, borderwidth=3)
        self.intro_label.config(font=('Courier', 14, 'bold'))
        self.intro_label.pack(pady=5)

        self.date_label = Label(
            self,
            text=f"1 Indian Rupee equals = {self.currency_converter.convert('INR','USD',1)} USD\nDate : {self.currency_converter.data['date']}",
            relief=tk.GROOVE, borderwidth=5
        )
        self.date_label.config(font=('Courier', 10))
        self.date_label.pack(pady=5)

        # Input area
        frame = Frame(self)
        frame.pack(pady=10)

        font = ("Courier", 11, "bold")
        self.option_add('*TCombobox*Listbox.font', font)

        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("🇮🇳 India (INR)")
        self.from_currency_dropdown = ttk.Combobox(
            frame, textvariable=self.from_currency_variable,
            values=list(country_currency_map.keys()), font=font,
            state='readonly', width=22, justify=tk.CENTER
        )
        self.from_currency_dropdown.grid(row=0, column=0, padx=10)

        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("🇺🇸 United States (USD)")
        self.to_currency_dropdown = ttk.Combobox(
            frame, textvariable=self.to_currency_variable,
            values=list(country_currency_map.keys()), font=font,
            state='readonly', width=22, justify=tk.CENTER
        )
        self.to_currency_dropdown.grid(row=0, column=1, padx=10)

        # Entry + Output fields
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(frame, bd=3, relief=tk.RIDGE, justify=tk.CENTER,
                                  validate='key', validatecommand=valid, font=font, width=20)
        self.amount_field.grid(row=1, column=0, pady=10)

        self.converted_amount_field_label = Label(frame, text='', fg='black', bg='white',
                                                  relief=tk.RIDGE, justify=tk.CENTER,
                                                  width=20, borderwidth=3, font=font)
        self.converted_amount_field_label.grid(row=1, column=1, pady=10)

        # Convert button
        self.convert_button = Button(self, text="Convert", fg="black", command=self.perform)
        self.convert_button.config(font=('Courier', 11, 'bold'), width=12)
        self.convert_button.pack(pady=5)

    def perform(self):
        try:
            amount = float(self.amount_field.get())
            from_curr = country_currency_map[self.from_currency_variable.get()]
            to_curr = country_currency_map[self.to_currency_variable.get()]
            converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
            self.converted_amount_field_label.config(text=str(round(converted_amount, 2)))
        except Exception:
            self.converted_amount_field_label.config(text="Invalid input")

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"^[0-9]*\.?[0-9]*$")
        result = regex.match(string)
        return (string == "" or result is not None)

if __name__ == "__main__":
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    app = App(converter)
    app.mainloop()


