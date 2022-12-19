import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
import re
from tkinter import *
import sys
window = Tk()
window.attributes("-topmost",True)
window.title("KZT - RUB")
window.geometry('300x26')
window.resizable(width=False, height=False)
lbl = Label(window, text="KZT:")
lbl.grid(column=0, row=0)
txt = Entry(window,width=15)
txt.grid(column=1, row=0)
lb2 = Label(window, text="RUB:")
lb2.grid(column=2, row=0)
txt2 = Entry(window,width=15)
txt2.grid(column=3, row=0)
def convertStr(if1):
    try:
        ret = int(if1)
    except ValueError:
        ret = float(if1)
    return ret
def get_exchange_list_xrates(currency, amount=1):
    content = requests.get(f"https://www.x-rates.com/table/?from={currency}&amount={amount}").content
    soup = bs(content, "html.parser")
    price_datetime = parse(soup.find_all("span", attrs={"class": "ratesTimestamp"})[1].text)
    exchange_tables = soup.find_all("table")
    exchange_rates = {}
    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            tds = tr.find_all("td")
            if tds:
                currency = tds[0].text
                exchange_rate = float(tds[1].text)
                exchange_rates[currency] = exchange_rate        
    return price_datetime, exchange_rates
def substring_after(s, delim):
    return s.partition(delim)[2]
def start():
    source_currency = 'KZT'
    amount = txt.get()
    if(int(convertStr(amount)) >= 1000000):
        amount = 1000000
    target_currency = "GBP"
    price_datetime, exchange_rates = get_exchange_list_xrates(source_currency, amount)
    txt2.delete(0, 'end')
    txt2.insert(0, re.sub("[, ']", '', substring_after(str(exchange_rates), "'Russian Ruble': ")[:8]))
btns = Button(window, text="Convert", command=start)
btns.grid(column=4, row=0)
window.mainloop()