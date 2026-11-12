
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from config.settings import BASE_URL, WAIT_TIMEOUT


class FormPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # Open website
    def open_website(self):
        self.driver.get(BASE_URL)

        self.wait.until(
            EC.presence_of_element_located(
                (By.NAME, "my-text")
            )
        )

    # Enter customer name
    def enter_customer_name(self, name):
        name_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "my-text")
            )
        )
        name_field.clear()
        name_field.send_keys(name)

    # Enter password
    def enter_password(self, password):
        password_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "my-password")
            )
        )
        password_field.send_keys(password)

    # Enter message
    def enter_message(self, message):
        message_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "my-textarea")
            )
        )
        message_field.send_keys(message)

    # Select dropdown option
    def select_dropdown(self, option_text):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "my-select")
            )
        )

        select = Select(dropdown)
        select.select_by_visible_text(option_text)

    # Select the second checkbox
    def select_checkbox(self):
        checkbox = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "my-check-2")
            )
        )

        if not checkbox.is_selected():
            checkbox.click()

        print("Checkbox selected:", checkbox.is_selected())

    # Select the second radio button
    def select_radio_button(self):
        radio = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "my-radio-2")
            )
        )

        if not radio.is_selected():
            radio.click()

        print("Radio button selected:", radio.is_selected())

    # Submit form
    def submit_form(self):
        submit_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit']")
            )
        )

        submit_button.click()

    # Verify form submission
    def verify_submission(self):
        result = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Received!']")
            )
        )

        return result.is_displayed()
