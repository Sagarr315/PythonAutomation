
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
        # Step 1: Start Edge
        driver = start_browser()
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Step 2: Open the official Selenium practice page
        driver.get(WEBSITE_URL)

        # Step 3: Wait for the Add button
        add_button = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "adder")
            )
        )

        print("Website opened successfully")

        # Step 4: Create a dynamic element
        add_button.click()

        # Step 5: Find elements using a partial ID
        dynamic_boxes = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[id^='box']")
            )
        )

        print("\n--- DYNAMIC ELEMENTS ---")

        for box in dynamic_boxes:

            print("ID:", box.get_attribute("id"))
            print("Class:", box.get_attribute("class"))

        # Step 6: Find the red box using its CSS class
        red_box = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".redbox")
            )
        )

        print("\nRed box found:", red_box.is_displayed())

        # Step 7: Reveal the hidden input
        reveal_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@id='reveal']")
            )
        )

        reveal_button.click()

        # Step 8: Find input using XPath
        input_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@id='revealed']")
            )
        )

        input_field.send_keys("Dynamic locator test")

        print("Entered text:", input_field.get_attribute("value"))

        # Step 9: Verify
        assert input_field.get_attribute("value") == "Dynamic locator test"

        # Step 10: Screenshot
        screenshot_dir = Path(SCREENSHOT_DIR)
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        screenshot_path = screenshot_dir / "dynamic_locators_success.png"

        driver.save_screenshot(str(screenshot_path))

        print("\nScreenshot:", screenshot_path)
        print("All dynamic locator tests passed!")

        logger.info("Dynamic locator exercise completed successfully")

    except Exception:

        logger.exception("Dynamic locator exercise failed")

        if driver:
            screenshot_dir = Path(SCREENSHOT_DIR)
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            driver.save_screenshot(
                str(screenshot_dir / "dynamic_locators_error.png")
            )

        raise

    finally:

        if driver:
            close_browser(driver)
            logger.info("Microsoft Edge closed")


if __name__ == "__main__":
    main()
