import pyautogui

from .config import SCREENSHOT_FILE, OUTPUT_DIR


def capture_full_screenshot():
    image = pyautogui.screenshot()
    image.save(SCREENSHOT_FILE)

    print("Screenshot saved:", SCREENSHOT_FILE)


def capture_region(x, y, width, height):
    image = pyautogui.screenshot(
        region=(x, y, width, height)
    )

    output_file = OUTPUT_DIR / "Region_Screenshot.png"
    image.save(output_file)

    print("Region screenshot saved:", output_file)


if __name__ == "__main__":
    capture_full_screenshot()