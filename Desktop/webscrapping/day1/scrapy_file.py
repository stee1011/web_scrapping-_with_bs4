import scrapy
from bs4 import BeautifulSoup

class BookSpider(scrapy.Spider):
    name = "book_spider"
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract book data
        for book in soup.find_all("article", class_="product_pod"):
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            stock = book.find("p", class_="instock availability").text.strip()
            relative_url = book.h3.a["href"]
            full_url = response.urljoin(relative_url)

            yield {
                "Title": title,
                "Price": price,
                "Stock": stock,
                "Book URL": full_url
            }

        # Find next page link
        next_page = soup.find("li", class_="next")
        if next_page:
            next_page_url = response.urljoin(next_page.a["href"])
            yield scrapy.Request(next_page_url, callback=self.parse)
