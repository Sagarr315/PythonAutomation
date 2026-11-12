import pyperclip


def copy_text(text):
    pyperclip.copy(text)
    print("Text copied to clipboard.")


def read_clipboard():
    text = pyperclip.paste()
    print("Clipboard content:", text)
    return text


def clear_clipboard():
    pyperclip.copy("")
    print("Clipboard cleared.")


if __name__ == "__main__":
    copy_text("Python Desktop Automation")
    read_clipboard()