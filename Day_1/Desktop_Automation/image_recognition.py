from pathlib import Path

import pyautogui

from .config import INPUT_DIR


def find_image(image_name):
    image_path = INPUT_DIR / image_name

    if not image_path.exists():
        print("Reference image not found:", image_path)
        return None

    try:
        position = pyautogui.locateOnScreen(str(image_path))

        if position is None:
            print("Image not found on screen.")
            return None

        print("Image found at:", position)
        return position

    except pyautogui.ImageNotFoundException:
        print("Image not found on screen.")
        return None


def click_image(image_name):
    position = find_image(image_name)

    if position:
        pyautogui.click(pyautogui.center(position))
        print("Image clicked successfully.")


if __name__ == "__main__":
    find_image("button.png")