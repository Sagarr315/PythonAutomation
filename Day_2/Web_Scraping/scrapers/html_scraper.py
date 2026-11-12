
from bs4 import BeautifulSoup


html_content = """
<html>
    <head>
        <title>Product Page</title>
    </head>

    <body>

        <h1>Product Information</h1>

        <div class="product">

            <h2>Laptop</h2>

            <p class="price">55000</p>

            <p class="rating">4.5</p>

        </div>

        <div class="product">

            <h2>Keyboard</h2>

            <p class="price">1200</p>

            <p class="rating">4.2</p>

        </div>

    </body>
</html>
"""


def scrape_html():

    soup = BeautifulSoup(html_content, "html.parser")

    # Extract page title
    page_title = soup.title.text

    print("Page Title:", page_title)

    # Extract heading
    heading = soup.find("h1")

    print("Heading:", heading.text)

    # Extract all products
    products = soup.find_all("div", class_="product")

    print("\n--- PRODUCT DETAILS ---")

    for product in products:

        name = product.find("h2").get_text(strip=True)

        price = product.find("p", class_="price").get_text(strip=True)

        rating = product.find("p", class_="rating").get_text(strip=True)

        print("Product:", name)
        print("Price:", price)
        print("Rating:", rating)
        print("--------------------")


if __name__ == "__main__":
    scrape_html()
