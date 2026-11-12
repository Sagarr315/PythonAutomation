
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser.driver import start_browser, close_browser
from utils.logger import get_logger
from config.settings import WAIT_TIMEOUT, SCREENSHOT_DIR


WEBSITE_URL = "https://www.selenium.dev/selenium/web/dynamic.html"


def main():

    logger = get_logger()
    driver = None

    try:
        # Step 1: Start browser
        logger.info("Starting Microsoft Edge")

        driver = start_browser()

        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Step 2: Open website
        driver.get(WEBSITE_URL)

        logger.info("Dynamic elements website opened")

        # Step 3: Click Add button
        add_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "adder")
            )
        )

        add_button.click()

        logger.info("Add button clicked")

        # Step 4: Wait for dynamically created box
        new_box = wait.until(
            EC.presence_of_element_located(
                (By.ID, "box0")
            )
        )

        box_class = new_box.get_attribute("class")

        print("Dynamic element ID:", new_box.get_attribute("id"))
        print("Dynamic element class:", box_class)

        logger.info("Dynamic box successfully detected")

        # Step 5: Click Reveal button
        reveal_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "reveal")
            )
        )

        reveal_button.click()

        logger.info("Reveal button clicked")

        # Step 6: Wait for hidden input to become visible
        input_field = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "revealed")
            )
        )

        # Step 7: Enter text
        input_field.send_keys(
            "Dynamic element handled successfully"
        )

        entered_value = input_field.get_attribute("value")

        print("Entered text:", entered_value)

        logger.info("Text entered into revealed input")

        # Step 8: Verify entered text
        if entered_value != "Dynamic element handled successfully":
            raise AssertionError("Input verification failed")

        # Step 9: Save screenshot
        screenshot_directory = Path(SCREENSHOT_DIR)
        screenshot_directory.mkdir(parents=True, exist_ok=True)

        screenshot_path = (
            screenshot_directory / "dynamic_elements_success.png"
        )

        driver.save_screenshot(str(screenshot_path))

        print("Screenshot saved:", screenshot_path)

        logger.info("Screenshot saved successfully")

        print("\nAll dynamic element tests passed!")

    except Exception:

        logger.exception("Dynamic element automation failed")

        if driver:
            error_directory = Path(SCREENSHOT_DIR)
            error_directory.mkdir(parents=True, exist_ok=True)

            error_path = error_directory / "dynamic_elements_error.png"

            driver.save_screenshot(str(error_path))

        raise

    finally:

        if driver:
            close_browser(driver)

            logger.info("Microsoft Edge closed")


if __name__ == "__main__":
    main()
