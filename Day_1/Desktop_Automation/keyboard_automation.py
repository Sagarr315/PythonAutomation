import time

import pyautogui
import pyperclip


def type_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    print("Text pasted successfully.")


def press_key(key):
    pyautogui.press(key)
    print("Key pressed:", key)


def press_shortcut(*keys):
    pyautogui.hotkey(*keys)
    print("Shortcut executed:", keys)


def type_into_notepad(text):
    subprocess_launch_notepad()
    time.sleep(2)

    type_text(text)

    print("Text entered into Notepad.")


def subprocess_launch_notepad():
    import subprocess
    subprocess.Popen(["notepad.exe"])


if __name__ == "__main__":
    type_into_notepad(
        "Hello! This is my first Python Desktop Automation Bot."
    )