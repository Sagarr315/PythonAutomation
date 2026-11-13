
import logging
import time
import requests

from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from Database_Automation.mini_projects.end_to_end_data_automation.config import (
    SCRAPING_BASE_URL,
    REQUEST_TIMEOUT
)


logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PythonAutomationPractice/1.0)"
}


# --------------------------------------------------
# 1. CLEAN BOOK DATA
# --------------------------------------------------

def clean_book(article, page_url):
    """
    Extract and validate one book from an HTML article.
    """

    title_element = article.select_one("h3 a")
    price_element = article.select_one(".price_color")
    rating_element = article.select_one(".star-rating")
    availability_element = article.select_one(".availability")

    if not title_element or not price_element:
        return None

    title = title_element.get("title", "").strip()

    if not title:
        return None

    # Extract numeric price from text such as £51.77
    price_text = price_element.get_text(strip=True)

    try:
        price = Decimal(
            price_text.replace("£", "").replace("Â", "").strip()
        )
    except InvalidOperation:
        logger.warning("Invalid price for book: %s", title)
        return None

    if not price.is_finite() or price < 0:
        return None

    # Extract star rating
    rating = "Unknown"

    if rating_element:

        rating_classes = rating_element.get("class", [])

        if len(rating_classes) > 1:
            rating = rating_classes[1]

    # Extract availability
    availability = "Unknown"

    if availability_element:
        availability = availability_element.get_text(
            " ",
            strip=True
        )

    # Convert relative URL into absolute URL
    relative_url = title_element.get("href", "")

    product_url = urljoin(page_url, relative_url)

    return {
        "title": title,
        "price": price,
        "currency": "GBP",
        "rating": rating,
        "availability": availability,
        "product_url": product_url,
        "source": "BooksToScrape"
    }


# --------------------------------------------------
# 2. SCRAPE ONE WEBSITE PAGE
# --------------------------------------------------

def scrape_page(session, page_url):
    """
    Download and extract books from one page.
    """

    response = session.get(
        page_url,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    articles = soup.select("article.product_pod")

    books = []

    for article in articles:

        book = clean_book(article, page_url)

        if book is not None:
            books.append(book)

    # Find next page link
    next_element = soup.select_one("li.next a")

    next_url = None

    if next_element:

        next_href = next_element.get("href")

        if next_href:
            next_url = urljoin(page_url, next_href)

    logger.info(
        "Scraped %s books from %s",
        len(books),
        page_url
    )

    return books, next_url


# --------------------------------------------------
# 3. SCRAPE MULTIPLE PAGES
# --------------------------------------------------

def scrape_books(max_pages=3):
    """
    Scrape multiple pages.

    max_pages controls how many pages are requested.
    """

    if max_pages <= 0:
        raise ValueError("max_pages must be greater than zero.")

    all_books = []

    current_url = SCRAPING_BASE_URL

    visited_urls = set()

    try:

        with requests.Session() as session:

            for page_number in range(1, max_pages + 1):

                if current_url in visited_urls:
                    logger.warning("Repeated page detected: %s", current_url)
                    break

                visited_urls.add(current_url)

                print(f"Scraping page {page_number}...")

                books, next_url = scrape_page(
                    session,
                    current_url
                )

                all_books.extend(books)

                if not next_url:
                    break

                current_url = next_url

                # Be considerate to the practice website.
                time.sleep(0.5)

        logger.info(
            "Total books extracted: %s",
            len(all_books)
        )

        return all_books

    except requests.exceptions.RequestException:

        logger.exception("Website request failed.")

        raise


# --------------------------------------------------
# 4. DISPLAY SCRAPED BOOKS
# --------------------------------------------------

def display_books(books, limit=5):

    print("\n--- SCRAPED BOOK DATA ---")

    if not books:
        print("No books found.")
        return

    for book in books[:limit]:

        print(
            f"Title: {book['title']}\n"
            f"Price: £{book['price']}\n"
            f"Rating: {book['rating']}\n"
            f"Availability: {book['availability']}\n"
            f"URL: {book['product_url']}\n"
        )

    print("Total books extracted:", len(books))


# --------------------------------------------------
# 5. MODULE TEST
# --------------------------------------------------

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    print("Starting web scraping...")

    try:

        books = scrape_books(max_pages=3)

        display_books(books)

        print("\nWeb scraping completed successfully!")

        return books

    except requests.exceptions.RequestException as error:

        print("\nWebsite connection error:", error)

    except ValueError as error:

        print("\nScraping configuration error:", error)

    return []


if __name__ == "__main__":
    main()
