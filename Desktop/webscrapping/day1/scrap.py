import requests
import lxml
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
headers = {'User-Agent':'Chrome'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "lxml")
    books = soup.find_all("article", class_="product_pod")
    filename = ("scrap.csv")
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title","Price","Stock availability","Link"])
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
        
            stock = book.find("p", class_="instock availability").text.strip()

            base_url = "https://books.toscrape.com/"


            book_url_ = book.h3.a.get("href")
            
            if book_url_.startswith("catalogue/"):
                full_url = url + book_url_
            else:
                full_url = url + "catalogue/" + book_url_

            writer.writerow([title, price, stock, full_url])

        print("Data saved to scrap.csv")



    

else:
    print("Error fetching the source code:")



