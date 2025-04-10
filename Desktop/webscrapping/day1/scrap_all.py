#a simple scrapping logic that extract book data from a website and save it to all_books.csv for demonstrating scrapping robot capabilities 
from bs4 import BeautifulSoup
import requests
import csv

#csv file name

filename = "all_books.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    #writting csv header
    writer.writerow(["Title","Price","Stock","Book_url"])

    #Now importing the data
    
    #defining server to browser communication env
    url = "https://books.toscrape.com/catalogue/page-{}.html"
    

    #if stat for err handling
    page = 1
    while True:
        #Definind the current url to work on 
        current_url = url.format(page)
        headers = {'User-Agent':'Chrome'}
        response = requests.get(current_url, headers=headers)

        if response.status_code == 200:
            #passind response data to BeautifulSoup method with lxml html phaser
            soup = BeautifulSoup(response.text, "lxml")
            #all books are under article tag with class name product_pod
            books = soup.find_all("article", class_="product_pod")
            #Iteration breaning
            
            #iterating for all books in each page
            for book in books:
                title = book.h3.a.get("title")
                price = book.find("p", class_="price_color").text.strip() if book.find("p", class_="price_color") else "N/A"
                stock = book.find("p", class_="instock availability").text.strip() if book.find("p", class_="instock availability") else "N/A"
                #url construction for book reference
                base_url = "https://books.toscrape.com/"
                relative_url = book.h3.a["href"]
                full_url = base_url + "catalogue/" + relative_url.lstrip("catalogue/")
                #writing extracted data to the csv file
                writer.writerow([title,price,stock,full_url])
        # logic to break the while loop to prevent server overloading
        elif not response.status_code == 404:

            # a possible error 404 meaning page not found is due to page depletion since there are 50 pages only in the web system

            print(f"Error :{response.status_code} maybe due to robot has finished extracting data...." )
            break

        else:
            print("Responce status from the server is: ",response.status_code)

        page += 1
    
            


    




