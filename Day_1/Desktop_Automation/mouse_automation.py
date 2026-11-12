import time

import pyautogui


def get_mouse_position():
    position = pyautogui.position()
    print("Mouse position:", position)
    return position


def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=1)
    print("Mouse moved to:", x, y)


def click_mouse(x=None, y=None):
    if x is not None and y is not None:
        pyautogui.click(x, y)
    else:
        pyautogui.click()

    print("Mouse clicked.")


def double_click_mouse(x=None, y=None):
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.doubleClick()

    print("Double click completed.")


def scroll_mouse(amount):
    pyautogui.scroll(amount)
    print("Mouse scrolled:", amount)


if __name__ == "__main__":
    time.sleep(3)
    get_mouse_position()
    move_mouse(500, 400)
    click_mouse()