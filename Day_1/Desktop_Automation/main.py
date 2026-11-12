from .application_automation import (
    launch_application,
    open_folder,
    list_running_applications,
)

from .mouse_automation import (
    get_mouse_position,
    move_mouse,
    click_mouse,
)

from .keyboard_automation import (
    type_into_notepad,
)

from .screenshot_automation import (
    capture_full_screenshot,
    capture_region,
)

from .clipboard_automation import (
    copy_text,
    read_clipboard,
)

from .window_automation import (
    list_windows,
    activate_window,
)

from .image_recognition import (
    find_image,
    click_image,
)

from .desktop_workflow import run_notepad_automation

from .config import OUTPUT_DIR, INPUT_DIR


def display_menu():
    print("\n====================================")
    print("     WINDOWS DESKTOP AUTOMATION")
    print("====================================")
    print("1. Launch Notepad")
    print("2. Launch Calculator")
    print("3. Launch Paint")
    print("4. Open File Explorer")
    print("5. List Running Applications")
    print("6. List Open Windows")
    print("7. Activate Notepad Window")
    print("8. Get Mouse Position")
    print("9. Move Mouse")
    print("10. Click Mouse")
    print("11. Capture Full Screenshot")
    print("12. Capture Screenshot Region")
    print("13. Copy Text to Clipboard")
    print("14. Read Clipboard")
    print("15. Type Text into Notepad")
    print("16. Find Image on Screen")
    print("17. Click Image on Screen")
    print("18. Open Input Folder")
    print("19. Run Complete Notepad Automation")
    print("0. Exit")
    print("====================================")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                launch_application("notepad")

            elif choice == "2":
                launch_application("calculator")

            elif choice == "3":
                launch_application("paint")

            elif choice == "4":
                launch_application("explorer")

            elif choice == "5":
                list_running_applications()

            elif choice == "6":
                list_windows()

            elif choice == "7":
                activate_window("Notepad")

            elif choice == "8":
                get_mouse_position()

            elif choice == "9":
                x = int(input("Enter X coordinate: "))
                y = int(input("Enter Y coordinate: "))
                move_mouse(x, y)

            elif choice == "10":
                x = int(input("Enter X coordinate: "))
                y = int(input("Enter Y coordinate: "))
                click_mouse(x, y)

            elif choice == "11":
                capture_full_screenshot()

            elif choice == "12":
                x = int(input("Enter X: "))
                y = int(input("Enter Y: "))
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))

                capture_region(x, y, width, height)

            elif choice == "13":
                text = input("Enter text to copy: ")
                copy_text(text)

            elif choice == "14":
                read_clipboard()

            elif choice == "15":
                text = input("Enter text for Notepad: ")
                type_into_notepad(text)

            elif choice == "16":
                image_name = input("Enter image filename: ")
                find_image(image_name)

            elif choice == "17":
                image_name = input("Enter image filename: ")
                click_image(image_name)

            elif choice == "18":
                open_folder(INPUT_DIR)

            elif choice == "19":
                confirmation = input(
                    "Open Notepad and save a demo file? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":
                    run_notepad_automation()
                else:
                    print("Automation cancelled.")

            elif choice == "0":
                print("Desktop Automation application closed.")
                break

            else:
                print("Invalid choice.")

        except (ValueError, OSError) as error:
            print("Operation failed:", error)

        except Exception as error:
            print("Unexpected error:", error)

        if choice != "0":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()