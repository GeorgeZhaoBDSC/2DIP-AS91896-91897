import tkinter as tk
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
    add_task_page.rowconfigure(2,minsize = 200, weight=2)
    add_task_page.rowconfigure(3,minsize = 100, weight=1)


    # The starting width of the window columns is 150/600px, and then expands with the ratio of 1:5
    add_task_page.columnconfigure(0, minsize = 150, weight=1)
    add_task_page.columnconfigure(1, minsize = 600, weight=5)

    # --------------------------------------- Title Bar --------------------------------------

    # Assigning properties to the title bar

    title_label = tk.Label(
        add_task_page,
        text="Add new task",
        padx=10,
        pady=10,
        font=("Times New Roman", 50),
        fg="white",
        bg="blue"
    )

    title_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # --------------------------------------- The Form --------------------------------------

    # Submit the info the user has entered in the 2 fields
    def submit_new_task():
        # Gets the info from the title entry and description entry
        title = title_entry.get("1.0", "end-1c")
        description = description_entry.get("1.0", "end-1c")

        # Clears the text boxes
        title_entry.delete("1.0", tk.END)
        description_entry.delete("1.0", tk.END)

        # Adds the new task to the list of tasks and also saves it to the json file
        add_new_task(title, description)

        # Refreshes the home page so that the new cards show up on the home page
        system_state["refresh_pages"]["home"]()

        # Switch back to the home page
        switch_page(system_state, "home")

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
    title_entry.grid(row=1, column=1, sticky="ew")

    description_label.grid(row=2, column=0, sticky="nsew")
    description_entry.grid(row=2, column=1, sticky="nsew")

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

    submit_button.grid(row=3, column=1)

    # --------------------------------------- Exit button --------------------------------------

    exit_button = tk.Button(
        add_task_page,
        text="Exit",
        command=lambda: switch_page(system_state, "home"),
        bg="green",
        fg="black",
        padx = 10,
        pady = 10,
    )

    exit_button.grid(row=3, column=0)

    return add_task_page

