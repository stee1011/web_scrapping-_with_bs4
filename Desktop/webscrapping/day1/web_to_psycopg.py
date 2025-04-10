import requests
import psycopg2
from bs4 import BeautifulSoup

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="stee1011",
    user="postgres",
    password="10110",
    host="localhost",
    port="3306"
)
cursor = conn.cursor()

# Define URL pattern
url = "https://books.toscrape.com/catalogue/page-{}.html"

page = 1
while True:
    current_url = url.format(page)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(current_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a.get("title")
            price = book.find("p", class_="price_color").text.strip() if book.find("p", class_="price_color") else "N/A"
            stock = book.find("p", class_="instock availability").text.strip() if book.find("p", class_="instock availability") else "N/A"
            base_url = "https://books.toscrape.com/"
            relative_url = book.h3.a["href"]
            full_url = base_url + "catalogue/" + relative_url.lstrip("catalogue/")

            # Insert data into PostgreSQL
            cursor.execute("""
                INSERT INTO books (title, price, stock, book_url)
                VALUES (%s, %s, %s, %s)
            """, (title, price, stock, full_url))

        conn.commit()

    elif response.status_code == 404:
        print(f"Scraping completed! Last page was {page - 1}")
        break

    else:
        print(f"Error {response.status_code}, stopping...")
        break

    page += 1

# Close DB connection
cursor.close()
conn.close()
print("Database connection closed.")
