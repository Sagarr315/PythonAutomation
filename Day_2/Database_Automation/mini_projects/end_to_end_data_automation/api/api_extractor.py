
import logging
import math
import requests

from Database_Automation.mini_projects.end_to_end_data_automation.config import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)


logger = logging.getLogger(__name__)

PRODUCTS_ENDPOINT = f"{API_BASE_URL}/products"


# --------------------------------------------------
# 1. VALIDATE AND CLEAN API PRODUCT DATA
# --------------------------------------------------

def clean_product(product):
    """
    Validate an API product and return selected fields.
    """

    if not isinstance(product, dict):
        return None

    product_id = product.get("id")
    title = product.get("title")
    price = product.get("price")

    if not isinstance(product_id, int) or product_id <= 0:
        return None

    if not isinstance(title, str) or not title.strip():
        return None

    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return None

    if not math.isfinite(price) or price < 0:
        return None

    return {
        "external_id": product_id,
        "title": title.strip(),
        "category": product.get("category"),
        "brand": product.get("brand"),
        "price": float(price),
        "stock": product.get("stock"),
        "rating": product.get("rating"),
        "source": "DummyJSON"
    }


# --------------------------------------------------
# 2. FETCH ONE PAGE OF PRODUCTS
# --------------------------------------------------

def fetch_products(session, limit=10, skip=0):
    """
    Fetch one page of products from DummyJSON.

    limit = number of records to request
    skip  = number of records to skip
    """

    if limit <= 0 or skip < 0:
        raise ValueError("Limit must be positive and skip cannot be negative.")

    response = session.get(
        PRODUCTS_ENDPOINT,
        params={
            "limit": limit,
            "skip": skip
        },
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("Unexpected API response format.")

    products = data.get("products")

    if not isinstance(products, list):
        raise ValueError("API response does not contain a valid products list.")

    cleaned_products = []

    for product in products:

        cleaned = clean_product(product)

        if cleaned is not None:
            cleaned_products.append(cleaned)
        else:
            logger.warning("Skipped an invalid API product.")

    logger.info(
        "Fetched %s valid products. Skip=%s",
        len(cleaned_products),
        skip
    )

    return cleaned_products, data.get("total", 0)


# --------------------------------------------------
# 3. FETCH ALL PRODUCTS USING PAGINATION
# --------------------------------------------------

def fetch_all_products(page_size=10):
    """
    Fetch products page by page until all records are retrieved.
    """

    if page_size <= 0:
        raise ValueError("Page size must be positive.")

    all_products = []
    skip = 0

    try:

        with requests.Session() as session:

            while True:

                products, total = fetch_products(
                    session=session,
                    limit=page_size,
                    skip=skip
                )

                all_products.extend(products)

                if not products:
                    break

                skip += page_size

                if skip >= total:
                    break

        logger.info(
            "Total valid products collected: %s",
            len(all_products)
        )

        return all_products

    except requests.exceptions.RequestException:

        logger.exception("API request failed.")

        raise

    except ValueError:

        logger.exception("API response validation failed.")

        raise


# --------------------------------------------------
# 4. DISPLAY API DATA
# --------------------------------------------------

def display_products(products, limit=5):

    print("\n--- API PRODUCT DATA ---")

    if not products:
        print("No valid products found.")
        return

    for product in products[:limit]:

        print(
            f"ID: {product['external_id']} | "
            f"Title: {product['title']} | "
            f"Category: {product['category']} | "
            f"Price: {product['price']}"
        )

    print("\nTotal products:", len(products))


# --------------------------------------------------
# 5. MODULE TEST
# --------------------------------------------------

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    print("Starting API extraction...")

    try:

        products = fetch_all_products(page_size=10)

        display_products(products)

        print("\nAPI extraction completed successfully!")

        return products

    except requests.exceptions.RequestException as error:

        print("\nAPI connection error:", error)

    except ValueError as error:

        print("\nAPI data error:", error)

    return []


if __name__ == "__main__":
    main()
