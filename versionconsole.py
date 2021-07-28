import requests
from bs4 import BeautifulSoup

import time
from plyer import notification

def notifyMe(title, message):
    notification.notify(
        title = title,
        message = message,
        app_icon = None, #"D:\\Python\\test\\newpricing.png"
        timeout = 10,
        )

url = input("Enter the amazon's url (press enter to skip) : ")
header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}

if url != "":
    response = requests.get(url, headers=header)
    if response.ok:
        with open("list_url.txt", "a") as file:
            file.write(f"{url}[{str(price_product)}\n")


while 1:
    file = open("list_url.txt",'r')
    for i in file:
        url, prix = i.split("[")
        response = requests.get(url, headers=header)
        if response.ok:
            soup = BeautifulSoup(response.text, "lxml")

            title_product = soup.find('span', attrs={"id": "productTitle"}).text
            price_product = soup.find("span", attrs={"id": "price_inside_buybox"}).text
            price_product = float(price_product[:len(price_product)-2].replace(",", "."))

        if float(prix) != price_product:
            print(f"--- NEW PRICE --- : {price_product}")
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
            print(f".........................")
            

    file.close()
    time.sleep(60)
