import subprocess
import time

import pyautogui
import pyperclip

from .config import NOTEPAD_FILE, SCREENSHOT_FILE


def run_notepad_automation():
    print("\nSTARTING DESKTOP AUTOMATION")

    print("Step 1: Launching Notepad")
    process = subprocess.Popen(["notepad.exe"])

    time.sleep(3)

    print("Step 2: Entering text")

    message = (
        "PYTHON DESKTOP AUTOMATION\n"
        "-------------------------\n"
        "Application: Notepad\n"
        "Automation: Python\n"
        "Task: Automatic text entry\n"
        "Status: Successful\n"
    )

    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")

    time.sleep(1)

    print("Step 3: Saving file")

    pyautogui.hotkey("ctrl", "s")
    time.sleep(2)

    pyperclip.copy(str(NOTEPAD_FILE))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    time.sleep(2)

    print("Step 4: Capturing screenshot")

    screenshot = pyautogui.screenshot()
    screenshot.save(SCREENSHOT_FILE)

    print("Notepad process ID:", process.pid)
    print("Text file saved:", NOTEPAD_FILE)
    print("Screenshot saved:", SCREENSHOT_FILE)

    print("\nDESKTOP AUTOMATION COMPLETED!")


if __name__ == "__main__":
    run_notepad_automation()