
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

from config.settings import HEADLESS, WAIT_TIMEOUT


def start_browser():

    # Project root directory
    project_root = Path(__file__).resolve().parents[1]

    # Edge WebDriver location
    driver_path = (
        project_root / "drivers" / "msedgedriver.exe"
    )

    # Verify driver exists
    if not driver_path.exists():
        raise FileNotFoundError(
            f"Edge WebDriver not found: {driver_path}"
        )

    # Edge browser options
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    # Explicit WebDriver service
    service = Service(
        executable_path=str(driver_path)
    )

    # Launch Microsoft Edge
    driver = webdriver.Edge(
        service=service,
        options=options
    )

    driver.implicitly_wait(0)

    driver.set_page_load_timeout(45)

    return driver


def close_browser(driver):

    if driver:
        driver.quit()
