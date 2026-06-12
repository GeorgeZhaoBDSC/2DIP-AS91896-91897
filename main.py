import tkinter as tk
from ui.pages_home_page_ui import create_home_page
from ui.pages_add_task_page_ui import create_add_task_page
from ui.pages_view_task_page import create_view_task_page

def main():
    # Create frame for all pages
    root = tk.Tk()
    root.title("To do list")

    # Configure dimensions for this frame that contains each page
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Create system_state, which stores variables and functions across different pages. All page can access this.
    system_state = {"root": root, "pages": {}, "refresh_pages": None, "task_list": None, "current_task": 0}

    # Add a common root frame for all the pages to use

    # Add the code for each page to system state.
    home, refresh_home = create_home_page(system_state)
    add_task = create_add_task_page(system_state)
    view_task, refresh_view_task = create_view_task_page(system_state)

    system_state["pages"] = {
        "home": home,
        "add_task": add_task,
        "view_task": view_task
    }

    system_state["refresh_pages"] = {
        "home": refresh_home,
        "add_task": lambda: None,
        "view_task": refresh_view_task
    }

    # Start on the home page
    home.tkraise()

    # Start UI
    root.mainloop()

if __name__ == "__main__":
    main()