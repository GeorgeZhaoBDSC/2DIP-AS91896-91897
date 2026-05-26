import tkinter as tk
from .backend.to_do_list_functions import *
from .backend.navigation import *

def create_view_task_page(system_state):

    root = system_state["root"]

    # ----------------------------------- General Page setup ---------------------------------
    # Create a add task page
    view_task_page = tk.Frame(root)

    # Places page in the root frame
    view_task_page.grid(row=0, column=0, sticky="nsew")

    # Expandable window: Top row stays constant width, the next 3 rows that contain the entry fields have width
    # 100/200/100 px respectively and expand with ratio 1:2:1
    view_task_page.rowconfigure(1,minsize = 100, weight=1)
    view_task_page.rowconfigure(2,minsize = 200, weight=2)
    view_task_page.rowconfigure(3,minsize = 100, weight=1)


    # The starting width of the window columns is 150/300/300px, and then expands with the ratio of 1:5:5
    view_task_page.columnconfigure(0, minsize = 150, weight=1)
    view_task_page.columnconfigure(1, minsize = 300, weight=5)
    view_task_page.columnconfigure(1, minsize = 300, weight=5)


    # --------------------------------------- Title Bar --------------------------------------

    # Assigning properties to the title bar

    title_label = tk.Label(
        view_task_page,
        text="Edit task",
        padx=10,
        pady=10,
        font=("Times New Roman", 50),
        fg="white",
        bg="blue"
    )

    title_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

    # -------------------------------- Display Task Information -------------------------------

    # Create a label for the text box below
    title_edit_label = tk.Label(
        view_task_page,
        text="Title: ",
        padx=20,
        pady=10,
    )

    # Create test box where the user can edit the task title
    title_edit_entry = tk.Text(
        view_task_page,
        height=2
    )

    # Create a label for the entry box where the user enters the description of the new task
    description_edit_label = tk.Label(
        view_task_page,
        text="Description:",
        padx=20,
        pady=10,
    )

    # Create the entry box where the user enters the description of the new task
    description_edit_entry = tk.Text(
        view_task_page,
        height=12
    )

    # Makes both text boxes sticky left to right, however title text box doesn't have to be very wide
    # so it is not sticky top to bottom like the description entry box
    title_edit_label.grid(row=1, column=0, sticky="ew")
    title_edit_entry.grid(row=1, column=1, columnspan=2, sticky="ew")

    description_edit_label.grid(row=2, column=0, sticky="ew")
    description_edit_entry.grid(row=2, column=1, columnspan=2, sticky="ew")

    # --------------------------------------- Save button --------------------------------------
    # Save the information about the task that the user changed
    def save_task_info():
        task_id = system_state["current_task"]

        # Gets the info from the title entry and description entry
        updated_title = title_edit_entry.get("1.0", "end-1c")
        updated_description = description_edit_entry.get("1.0", "end-1c")

        edit_task(task_id, updated_title, updated_description)

        # Refresh the home page card scroll bar so update shows up
        system_state["refresh_pages"]["home"]()


    # Button that saves the entry the user has edited
    save_button = tk.Button(
        view_task_page,
        text="Save Changes",
        command=lambda: save_task_info(),
        bg="green",
        fg="black",
        padx = 15,
        pady = 10,
    )

    save_button.grid(row=3, column=2)

    # --------------------------------------- Delete button --------------------------------------
    # Deletes the task and clears entry box
    def delete_task_info():
        task_id = system_state["current_task"]

        title_edit_entry.delete("1.0", tk.END)
        description_edit_entry.delete("1.0", tk.END)

        # Deletes the task from the list of tasks and json file
        delete_task(task_id)

        # Refresh the home page card scroll bar so update shows up
        system_state["refresh_pages"]["home"]()

        # Returns back to the home page since there is no task to display
        switch_page(system_state, "home")

    # Button that saves the entry the user has edited
    delete_button = tk.Button(
        view_task_page,
        text="Delete task",
        command=lambda: delete_task_info(),
        bg="green",
        fg="black",
        padx = 15,
        pady = 10,
    )

    delete_button.grid(row=3, column=1)

    # --------------------------------------- Exit button --------------------------------------

    exit_button = tk.Button(
        view_task_page,
        text="Exit",
        command=lambda: switch_page(system_state, "home"),
        bg="green",
        fg="black",
        padx = 10,
        pady = 10,
    )

    exit_button.grid(row=3, column=0)

    def refresh_view_task_page_text():
        # Add the information about the current task for the user to view and edit from the View Task button on the home page

        task_id = system_state["current_task"]

        # Delete text in the entry boxes
        # Clears the title and description entry boxes on the view task page
        title_edit_entry.delete("1.0", tk.END)
        description_edit_entry.delete("1.0", tk.END)

        # Insert the correct text back in
        # Writes new title and description into those 2 entry boxes on the view task page
        title_edit_entry.insert("1.0", task_list[task_id]["title"])
        description_edit_entry.insert("1.0", task_list[task_id]["description"])

    return view_task_page, refresh_view_task_page_text