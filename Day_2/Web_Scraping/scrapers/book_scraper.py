
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup


WEBSITE_URL = "https://books.toscrape.com/"


def load_html():

    # Step 1: Find project directory
    project_root = Path(__file__).resolve().parents[1]

    # Step 2: Locate downloaded HTML
    html_file = project_root / "output" / "website_response.html"

    if not html_file.exists():
        raise FileNotFoundError(
            f"HTML file not found: {html_file}. "
            "Run live_request.py first."
        )

    # Step 3: Read HTML
    with open(html_file, "r", encoding="utf-8") as file:
        return file.read()


def scrape_books():

    # Step 4: Load HTML
    html_content = load_html()

    # Step 5: Parse HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Step 6: Find all book containers
    book_elements = soup.select("article.product_pod")

    books = []

    print("--- EXTRACTED BOOK DETAILS ---\n")

    # Step 7: Process each book
    for book in book_elements:

        # Extract title
        title_element = book.select_one("h3 a")

        title = (
            title_element.get("title", "").strip()
            if title_element else "Unknown"
        )

        # Extract price
        price_element = book.select_one("p.price_color")

        price = (
            price_element.get_text(strip=True)
            if price_element else "Unknown"
        )

        # Extract rating
        rating_element = book.select_one("p.star-rating")

        rating = "Unknown"

        if rating_element:
            rating_classes = rating_element.get("class", [])
            rating = next(
                (value for value in rating_classes if value != "star-rating"),
                "Unknown"
            )

        # Extract availability
        availability_element = book.select_one(
            "p.instock.availability"
        )

        availability = (
            availability_element.get_text(strip=True)
            if availability_element else "Unknown"
        )

        # Extract product URL
        product_url = ""

        if title_element and title_element.get("href"):
            product_url = urljoin(
                WEBSITE_URL,
                title_element["href"]
            )

        # Store extracted data
        book_data = {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "product_url": product_url
        }

        books.append(book_data)

        # Display each book
        print("Title:", title)
        print("Price:", price)
        print("Rating:", rating)
        print("Availability:", availability)
        print("URL:", product_url)
        print("-" * 60)

    # Step 8: Display summary
    print("\n--- SCRAPING SUMMARY ---")
    print("Total books extracted:", len(books))

    return books


if __name__ == "__main__":
    scrape_books()
