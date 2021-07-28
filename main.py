import requests
from bs4 import BeautifulSoup

import time
from plyer import notification
from tkinter import *


def notifyMe(title, message):
    notification.notify(
        title = title,
        message = message,
        app_icon = None, #"D:\\Python\\test\\newpricing.png"
        timeout = 10,
        )

header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}

timewait = time.time()
runscrap = 0



def add_url():
    if url.get() != "":
        response = requests.get(url.get(), headers=header)
        if response.ok:
            print(url.get())
            soup = BeautifulSoup(response.text, "lxml")
            try:

                title_product = soup.find('span', attrs={"id": "productTitle"}).text
                price_product = soup.find("span", attrs={"id": "price_inside_buybox"}).text
                price_product = float(price_product[:len(price_product)-2].replace(",", "."))

                with open("list_url.txt", "a") as file:
                    file.write(f"{url.get()}[{str(price_product)}\n")
            except:
                try:
                    title_product = soup.find('span', attrs={"id": "productTitle"}).text
                    price_product = soup.find("span", attrs={"id": "price"}).text
                    price_product = float(price_product[:len(price_product)-2].replace(",", "."))

                    with open("list_url.txt", "a") as file:
                        file.write(f"{url.get()}[{str(price_product)}\n")
                except:
                    print("error")

def run():
    global timewait
    if time.time() > timewait and runscrap == 1:
        timewait = time.time() + 60
        file = open("list_url.txt",'r')

        for i in file:
            url, prix = i.split("[")
            response = requests.get(url, headers=header)
            if response.ok:
                soup = BeautifulSoup(response.text, "lxml")

                try:
                    title_product = soup.find('span', attrs={"id": "productTitle"}).text
                    price_product = soup.find("span", attrs={"id": "price_inside_buybox"}).text
                except:
                    title_product = soup.find('span', attrs={"id": "productTitle"}).text
                    price_product = soup.find("span", attrs={"id": "price"}).text
                price_product = float(price_product[:len(price_product)-2].replace(",", "."))


            if float(prix) != price_product:
                label = f"--- NEW PRICE --- : {price_product}"
                label = Label(root, text=label)
                label.pack()

                notifyMe("New Price", f"{title_product[:50]}... : {price_product}")

                f = open('list_url.txt','r')
                lst = []
                for line in f:
                    if i in line:
                        line = line.replace(i,"")
                        lst.append(f"{url}[{price_product}")
                    lst.append(line)
                f.close()
                f = open('list_url.txt','w')
                for line in lst:
                    f.write(line)

                f.close()
                list_url.append(f"{url}[{price_product}")
            else:
                print("non")
            

        file.close()
    

def stop():
    global runscrap
    if runscrap == 1:
        runbtntext.set("RUN")
        runscrap = 0
        print("Stop")
    elif runscrap == 0:
        runbtntext.set("STOP")
        runscrap = 1
        print("Run")


root = Tk(className='Amazon price traker')
root.wm_iconbitmap('Uiconstock-Socialmedia-Amazon.ico')
root.minsize(700, 250)
root.maxsize(700, 250)

runbtntext = StringVar()
runbtntext.set("RUN")

label = Label(root, text="Enter a new amazon's url")
label.pack(pady = 10)
label.config(font=('Courier',20))

url = Entry(root, width=25, font=('Courier',20))
url.pack(pady = 10)

addurlbtn = Button(root, text="Add url", command=add_url)
addurlbtn.pack(pady = 10)
addurlbtn.config(font=('Courier',15))

runbtn = Button(root, textvariable=runbtntext, command=stop)
runbtn.pack(pady = 10)
runbtn.config(font=('Courier',15))




while 1:

    run()
    root.update()
    
