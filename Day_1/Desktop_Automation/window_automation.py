from pywinauto import Desktop


def list_windows():
    desktop = Desktop(backend="uia")

    print("\n--- Available Windows ---")

    for window in desktop.windows():
        title = window.window_text()

        if title.strip():
            print(title)


def activate_window(title_keyword):
    desktop = Desktop(backend="uia")

    for window in desktop.windows():
        title = window.window_text()

        if title_keyword.lower() in title.lower():
            try:
                window.set_focus()
                print("Activated window:", title)
                return True

            except Exception as error:
                print("Could not activate window:", error)
                return False

    print("Window not found:", title_keyword)
    return False


if __name__ == "__main__":
    list_windows()
    activate_window("Notepad")