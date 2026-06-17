import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
from .backend.to_do_list_functions import *
from .backend.navigation import *

def create_add_task_page(system_state):

    root = system_state["root"]

    # ----------------------------------- General Page setup ---------------------------------
    # Create a add task page
    add_task_page = tk.Frame(root)

    # Places page in the root frame
    add_task_page.grid(row=0, column=0, sticky="nsew")

    # Expandable window: Top row stays constant width, the next 3 rows that contain the entry fields have width
    # 100/200/100 px respectively and expand with ratio 1:2:1
    add_task_page.rowconfigure(1,minsize = 100, weight=1)
    add_task_page.rowconfigure(2,minsize = 150, weight=2)
    add_task_page.rowconfigure(3, minsize=50, weight=1)
    add_task_page.rowconfigure(4,minsize = 100, weight=1)


    # The starting width of the window columns is 150/600px, and then expands with the ratio of 1:5
    add_task_page.columnconfigure(0, minsize = 150, weight=1)
    add_task_page.columnconfigure(1, pad=20, minsize = 600, weight=5)


    # --------------------------------------- Submit Function --------------------------------------

    # Submit the info the user has entered in all the fields of the form
    def submit_new_task():
        task_id = system_state["current_task"]
        # Check the validity of the input
        valid_input = check_input_validity()
        if not valid_input:
            return

        # Gets the info from the title entry and description entry
        title = title_entry.get("1.0", "end-1c")
        description = description_entry.get("1.0", "end-1c")

        # Clears the text boxes
        title_entry.delete("1.0", tk.END)
        description_entry.delete("1.0", tk.END)

        # Gets the priority option the user inputs
        priority = selected_priority.get()

        # Resets the priority option back to the first option
        selected_priority.set(PRIORITY_OPTIONS[0])

        # Gets the due date from the calender dropdown
        due_date = date_entry.get_date()

        # Store the date in a better way so it doesn't break the JSON file
        stored_date = due_date.strftime("%Y-%m-%d")
        # Resets the date back to the default date (current date)
        date_entry.set_date(date.today())

        # Adds the new task to the list of tasks and also saves it to the json file
        add_new_task(title, description, priority, stored_date, task_id[0])

        # Refreshes the home page so that the new cards show up on the home page
        system_state["refresh_pages"]["home"]()

        # Switch back to the home page
        switch_page(system_state, "home")

    # A function to check whether the input is valid
    def check_input_validity():
        # Get the title, description, and due date the user has input
        title = title_entry.get("1.0", "end-1c")
        description = description_entry.get("1.0", "end-1c")
        due_date = date_entry.get_date()

        # If current date is after the due date, return invalid input and notify user
        today = date.today()
        if due_date < today:
            messagebox.showinfo("!!", "The due date you have entered is in the past.")
            return False

        # If title is blank, notify user, return invalid input
        if title == "":
            messagebox.showinfo("!!", "Please enter a title")
            return False

        # If description is blank, notify user, give option to continue without a descrpiton
        if description == "":
            return messagebox.askyesno("!!", "Your task does not have description. Do yo want to save the task?")

        return True


    # --------------------------------------- Title Bar --------------------------------------

    # Assigning properties to the title bar

    title_bar = tk.Frame(
        add_task_page,
        padx=10,
        pady=20,
        height = 100,
        bg="lightgrey"
    )

    title_bar.grid_columnconfigure(0, weight=1)

    title_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

    title_label = tk.Label(
        title_bar,
        text="Add Task",
        font=TITLE_FONT,
        fg="black",
        bg="lightgrey",
        relief="flat",
        anchor="center",
        justify="center",
    )

    # Place title text in the title grid area
    title_label.grid(row=0, column=0, sticky="")

    # ------------------------------------ Title/Description Entry -----------------------------------

    # Create a label for the entry box where the user enters the title of the new task
    title_label = tk.Label(
        add_task_page,
        text="Title: ",
        padx=20,
        pady=10,
    )

    # Create entry box where the user enters the title of the new task
    title_entry = tk.Text(
        add_task_page,
        height = 2,
    )

    # Create a label for the entry box where the user enters the description of the new task
    description_label = tk.Label(
        add_task_page,
        text="Description:",
        padx=20,
        pady=10,
    )

    # Create the entry box where the user enters the description of the new task
    description_entry = tk.Text(
        add_task_page,
        height = 12,
    )

    # Makes both text entry boxes sticky left to right, however title entry box doesn't have to be very wide
    # so it is not sticky top to bottom like the description entry box
    title_label.grid(row=1, column=0, sticky="ew")
    title_entry.grid(row=1, column=1, sticky="ew", padx=(0, 20))

    description_label.grid(row=2, column=0, sticky="nsew")
    description_entry.grid(row=2, column=1, sticky="nsew", padx=(0, 20))

    # Button that submits the entry
    submit_button = tk.Button(
        add_task_page,
        text="Submit",
        command=lambda: submit_new_task(),
        bg="green",
        fg="black",
        padx = 15,
        pady = 10,
    )

    submit_button.grid(row=4, column=1)

    # --------------------------------------- Dropdown select --------------------------------------

    # Add a frame for the dropdown select buttons
    dropdown_area = tk.Frame(
        add_task_page,
        padx=10,
        pady=10,
    )

    dropdown_area.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="nsew"
    )

    # Define the sizes of the columns in this nested grid
    dropdown_area.columnconfigure(0, weight=1)
    dropdown_area.columnconfigure(1, weight=1)

    # Priority Select button
    # variable to store the selected option
    selected_priority = tk.StringVar()
    selected_priority.set(PRIORITY_OPTIONS[0])

    # Create dropdown
    # The last element is removed as it is COMPLETE. The program does not allow the user to add a task that is already done.
    dropdown = tk.OptionMenu(
        dropdown_area,
        selected_priority,
        *PRIORITY_OPTIONS[:-1],
    )

    # Places the dropdown into the grid
    dropdown.grid(
        row=1,
        column=0,
        padx = 10,
        pady = 10,
        sticky=""
    )

    # Due Date Select button
    date_entry = DateEntry(
        dropdown_area,
        width=12
    )
    # Places the dropdown into the grid
    date_entry.grid(
        row=1,
        column=1,
        pady=20,
        padx=20,
    )

    # Created labels for the two dropdowns

    priority_label = tk.Label(
        dropdown_area,
        text="Importance: ",
        font=TEXT_FONT,
        fg="black",
    )
    priority_label.grid(row=0, column=0, sticky="")

    date_label = tk.Label(
        dropdown_area,
        text="Due date: ",
        font=TEXT_FONT,
        fg="black",
    )
    date_label.grid(row=0, column=1, sticky="")

    # --------------------------------------- Exit button --------------------------------------

    exit_button = tk.Button(
        add_task_page,
        text="Home",
        command=lambda: switch_page(system_state, "home"),
        bg="green",
        fg="black",
        padx = 10,
        pady = 10,
    )

    exit_button.grid(row=4, column=0)

    return add_task_page