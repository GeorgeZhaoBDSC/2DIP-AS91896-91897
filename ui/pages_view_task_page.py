import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
from datetime import datetime as dt
from .backend.to_do_list_functions import *
from .backend.navigation import *
from .backend. refresh import *

def create_view_task_page(system_state):
    # ============================================= CREATE PAGE =============================================

    root = system_state["root"]
    # Create an add task page
    view_task_page = tk.Frame(root)

    # ============================================= PAGE SETUP =============================================

    def page_setup():
        # Places page in the root frame
        view_task_page.grid(row=0, column=0, sticky="nsew")

        # Expandable window: Top row stays constant width, the next 3 rows that contain the entry fields have width
        # 100/200/100 px respectively and expand with ratio 1:2:1
        view_task_page.rowconfigure(1,minsize = 100, weight=1)
        view_task_page.rowconfigure(2,minsize = 150, weight=2)
        view_task_page.rowconfigure(3,minsize = 50, weight=1)
        view_task_page.rowconfigure(4, minsize=100, weight=1)


        # The starting width of the window columns is 150/300/300px, and then expands with the ratio of 1:5:5
        view_task_page.columnconfigure(0, minsize = 150, weight=1)
        view_task_page.columnconfigure(1, minsize = 200, weight=2)
        view_task_page.columnconfigure(2, minsize = 200, weight=2)
        view_task_page.columnconfigure(3, minsize=200, weight=2)

    # ============================================= PAGE CONTENTS =============================================

    def create_save_button(entries):
        title_edit_entry, description_edit_entry, selected_priority, date_entry = entries
        # Save the information about the task that the user changed
        def save_task_info():
            task_id = system_state["current_task"]
            # Check the validity of the input
            valid_input = check_input_validity()
            if not valid_input:
                return

            # Gets the info from the title entry and description entry
            updated_title = title_edit_entry.get("1.0", "end-1c")
            updated_description = description_edit_entry.get("1.0", "end-1c")

            # Gets the priority option the user inputs
            priority = selected_priority.get()

            # Gets the due date from the calender dropdown
            due_date = date_entry.get_date()

            # Store the date in a better way so it doesn't break the JSON file
            stored_date = due_date.strftime("%Y-%m-%d")

            edit_task(task_id, updated_title, updated_description, priority, stored_date)

            # Refresh the home page card scroll bar so update shows up
            system_state["refresh_pages"]["home"]()

            # Switch back to the home page
            switch_page(system_state, "home")

        def check_input_validity():
            # Get the title, description, and due date the user has input
            title = title_edit_entry.get("1.0", "end-1c")
            description = description_edit_entry.get("1.0", "end-1c")
            due_date = date_entry.get_date()

            # If current date is after the due date, return invalid input and notify user
            today = date.today()
            if due_date < today:
                return messagebox.askyesno("!!", "Your task is overdue. Do you want to change the due date?")

            # If title is blank, notify user, return invalid input
            if title == "":
                messagebox.showinfo("!!", "Please enter a title")
                return False

            # If description is blank, notify user, give option to continue without a descrpiton
            if description == "":
                return messagebox.askyesno("!!", "Your task does not have description. Do you want to save the task?")

            return True

        # Button that saves the entry the user has edited
        save_button = tk.Button(
            view_task_page,
            text="Save Changes",
            command=lambda: save_task_info(),
            bg="lightgrey",
            fg="black",
            padx=15,
            pady=10,
        )

        save_button.grid(row=4, column=2)

    # --------------------------------------- Delete button --------------------------------------
    def create_delete_button():
        # Deletes the task and clears entry box
        def delete_task_info():
            task_id = system_state["current_task"]

            # Ask the user if they confirm they want to delete the task
            if not messagebox.askyesno("!!", "Are you sure you want to delete this task?"):
                return

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
            bg="lightgrey",
            fg="black",
            padx=15,
            pady=10,
        )

        delete_button.grid(row=4, column=1)

    # --------------------------------------- Title Bar --------------------------------------
    def create_title_bar():
        # Assigning properties to the title bar

        title_bar = tk.Frame(
            view_task_page,
            padx=10,
            pady=20,
            height=100,
            bg="lightgrey"
        )

        title_bar.grid_columnconfigure(0, weight=1)

        title_bar.grid(row=0, column=0, columnspan=4, sticky="nsew")

        title_label = tk.Label(
            title_bar,
            text="Edit Task",
            font=TITLE_FONT,
            fg="black",
            bg="lightgrey",
            relief="flat",
            anchor="center",
            justify="center",
        )

        # Place title text in the title grid area
        title_label.grid(
            row=0,
            column=0,
            sticky=""
        )

    # -------------------------------- Display Task Information -------------------------------
    def create_entry_fields():
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
        title_edit_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=(0, 20))

        description_edit_label.grid(row=2, column=0, sticky="ew")
        description_edit_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=(0, 20))


        # --------------------------------------- Dropdown select --------------------------------------

        # Add a frame for the dropdown select buttons
        dropdown_area = tk.Frame(
            view_task_page,
            padx=10,
            pady=10,
        )

        dropdown_area.grid(row=3,column=0,columnspan=4,sticky="nsew")

        # Define the sizes of the columns in this nested grid
        dropdown_area.columnconfigure(0, weight=1)
        dropdown_area.columnconfigure(1, weight=1)

        # Priority Select button
        # variable to store the selected option
        selected_priority = tk.StringVar()
        selected_priority.set(PRIORITY_OPTIONS[0])

        # Create dropdown
        dropdown = tk.OptionMenu(
            dropdown_area,
            selected_priority,
            *PRIORITY_OPTIONS,
        )

        # Places the dropdown into the grid
        dropdown.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
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

        return title_edit_entry, description_edit_entry, selected_priority, date_entry

    # --------------------------------------- Exit button --------------------------------------
    def create_exit_button(entries):
        title_edit_entry, description_edit_entry, selected_priority, date_entry = entries
        # A function that activates when the user exits the task
        def exit_task():
            # Reassign the task_id that might have changed.
            task_id = system_state["current_task"]

            # Gets the info from the title entry and description entry
            updated_title = title_edit_entry.get("1.0", "end-1c")
            updated_description = description_edit_entry.get("1.0", "end-1c")

            # Gets the priority option the user inputs
            priority = selected_priority.get()

            # Gets the due date from the calendar dropdown
            due_date = date_entry.get_date()

            # Store the date in a better way so it doesn't break the JSON file
            stored_date = due_date.strftime("%Y-%m-%d")

            # Check if the user has made any changes to any of the fields
            changes = updated_title != list(task_list.values())[task_id[0]][task_id[1]]["title"] or updated_description != list(task_list.values())[task_id[0]][task_id[1]]["description"] or priority != list(task_list.values())[task_id[0]][task_id[1]]["priority"] or stored_date != list(task_list.values())[task_id[0]][task_id[1]]["date"]

            if changes:
                if messagebox.askyesno("!!", "You have unsaved changes. Would you like to save before exiting?"):
                    return

            # Switch back to the home page
            switch_page(system_state, "home")

        exit_button = tk.Button(
            view_task_page,
            text="Home",
            command=lambda: exit_task(),
            bg="lightgrey",
            fg="black",
            padx = 10,
            pady = 10,
        )

        exit_button.grid(row=4, column=0)

    # --------------------------------------- Finish button --------------------------------------
    def create_finish_button():
        # Reassign the task_id that might have changed.
        task_id = system_state["current_task"]

        # Do not create a finish button if this task is already in the finished list
        if task_id[0] == len(task_list) - 1:
            return

        # A function that activates when the user presses finish task
        def finish_task():
            # Reassign the task_id that might have changed.
            task_id = system_state["current_task"]

            # Mark the task as done by moving it to the finished list
            mark_as_done(task_id)

            # Refresh the home page card scroll bar so update shows up
            system_state["refresh_pages"]["home"]()

            # Switch back to the home page
            switch_page(system_state, "home")

        finish_button = tk.Button(
            view_task_page,
            text="Complete",
            command=lambda: finish_task(),
            bg="lightgrey",
            fg="black",
            padx=10,
            pady=10,
        )

        finish_button.grid(row=4, column=3)

    def add_task_info(entries):
        title_edit_entry, description_edit_entry, selected_priority, date_entry = entries
        # Reassign the task_id that might have changed.
        task_id = system_state["current_task"]

        # Add the information about the current task for the user to view and edit from the View Task button on the home page

        # Delete text in the entry boxes
        # Clears the title and description entry boxes on the view task page
        title_edit_entry.delete("1.0", tk.END)
        description_edit_entry.delete("1.0", tk.END)

        # Find the list the task is in
        current_list = list(task_list.values())[task_id[0]]

        if not current_list:
            return

        # Insert the correct text back in
        # Writes new title and description into those 2 entry boxes on the view task page
        title_edit_entry.insert("1.0", current_list[task_id[1]]["title"])
        description_edit_entry.insert("1.0", current_list[task_id[1]]["description"])

        # Write the selected priority option into the priority box
        selected_priority.set(current_list[task_id[1]]["priority"])

        stored_date = current_list[task_id[1]]["date"]
        # Convert the stored date format back into a DateEntry usable format
        due_date = dt.strptime(stored_date, "%Y-%m-%d").date()

        # Write the date into the date entry field
        date_entry.set_date(due_date)

    # ====================================== COMPILE FUNCTIONS & LOAD PAGE ======================================
    # Compile all elements of the page
    def build_page():
        create_title_bar()
        entries = create_entry_fields()
        create_exit_button(entries)
        create_delete_button()
        create_finish_button()
        create_save_button(entries)
        add_task_info(entries)

    # Refresh page by passing all elements of the page into the refresh function where the refresh page function
    # Deletes all elements and rebuilds it using the build_page() function
    def refresh_page():
        refresh(view_task_page, build_page)

    # Build and refresh the page to start with
    page_setup()
    build_page()

    return view_task_page, refresh_page