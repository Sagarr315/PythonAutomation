from pathlib import Path

from browser.driver import start_browser, close_browser
from pages.form_page import FormPage
from utils.logger import get_logger

from config.settings import SCREENSHOT_DIR


def main():

    logger = get_logger()

    driver = None

    try:

        logger.info("Starting web automation")

        # Step 1: Start browser
        driver = start_browser()

        logger.info("Chrome browser started")

        # Step 2: Create page object
        form_page = FormPage(driver)

        # Step 3: Open website
        form_page.open_website()

        logger.info("Website opened successfully")

        # Step 4: Enter customer information
        form_page.enter_customer_name(
            "John Smith"
        )

        form_page.enter_password(
            "TestPassword123"
        )

        form_page.enter_message(
            "This is an automated test submission."
        )

        logger.info("Customer information entered")

        # Step 5: Select dropdown
        form_page.select_dropdown("Two")

        logger.info("Dropdown selected")

        # Step 6: Select checkbox
        form_page.select_checkbox()

        logger.info("Checkbox handled")

        # Step 7: Select radio button
        form_page.select_radio_button()

        logger.info("Radio button handled")

        # Step 8: Submit form
        form_page.submit_form()

        logger.info("Form submitted")

        # Step 9: Verify submission
        success = form_page.verify_submission()

        if success:

            logger.info(
                "Form submission verified successfully"
            )

        else:

            logger.error(
                "Form submission verification failed"
            )

        # Step 10: Capture screenshot
        screenshot_directory = Path(SCREENSHOT_DIR)

        screenshot_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        screenshot_path = (
            screenshot_directory / "form_success.png"
        )

        driver.save_screenshot(
            str(screenshot_path)
        )

        logger.info(
            "Screenshot saved: %s",
            screenshot_path
        )

        logger.info("Automation completed successfully")

    except Exception:

        logger.exception("Automation failed")

        if driver:

            error_path = (
                Path(SCREENSHOT_DIR) / "error.png"
            )

            error_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            driver.save_screenshot(str(error_path))

    finally:

        # Step 11: Close browser
        close_browser(driver)

        logger.info("Browser closed")


if __name__ == "__main__":

    main()
