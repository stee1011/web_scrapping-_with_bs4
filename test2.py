import csv
import bs4 as BeautifulSoup
from fake_useragent import UserAgent 
import requests
from urllib.parse import urljoin

# Setup session with headers
session = requests.Session()
ua = UserAgent()

session.headers.update({
    "User-Agent": ua.random,
    "Accept-Language": "en-US,en",
    "Accept-Encoding": "UTF-8",
    "Connection": "keep-alive"
})

def get_page(url):
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            return response.text, response.status_code
        elif response.status_code == 429:
            print("Rate limit hit.")
        else:
            print(f"Server error: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None, None

def extract_books(soup):
    books = soup.find_all("article", class_="product_pod")
    data = []
    for book in books:
        name = book.h3.a["title"]
        price = book.find("p", class_="price_color").get_text(strip=True)
        instock = book.find("p", class_="instock availability").get_text(strip=True)
        data.append([name, price, instock])
    return data

def extract_the_web(base_url):
    curr_url = base_url
    all_books = []

    while True:
        html, code = get_page(curr_url)
        if code != 200 or not html:
            break
        
        soup = BeautifulSoup.BeautifulSoup(html, 'lxml')
        books = extract_books(soup)
        all_books.extend(books)
        
        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_link = next_btn.a['href']
            curr_url = urljoin(curr_url, next_link)
        else:
            break

    return all_books

def write_to_csv(data, filename="books.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "price", "instock"])
        writer.writerows(data)
    print(f"Done. {len(data)} books written to {filename}")

if __name__ == "__main__":
    base_url = "https://books.toscrape.com/"
    all_books = extract_the_web(base_url)
    if all_books:
        write_to_csv(all_books)

