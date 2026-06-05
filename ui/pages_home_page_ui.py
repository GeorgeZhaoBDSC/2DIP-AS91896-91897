import tkinter as tk
from .backend.to_do_list_functions import *
from .backend.navigation import *

def create_home_page(system_state):

    # Create root inside the home page function
    root = system_state["root"]

    # ----------------------------------- General Page setup ---------------------------------
    # Create a home page
    home_page = tk.Frame(root)

    # Places homepage in the root frame
    home_page.grid(row=0, column=0, sticky="nsew")

    # Expandable window: Top row remains the same width, second row expands, starting at height of 400px
    home_page.rowconfigure(1,minsize = 400, weight=1)

    # The starting width of the window columns is 250/500px, and then expands with the ratio of 1:5
    home_page.columnconfigure(0, minsize = 250, weight=1)
    home_page.columnconfigure(1, minsize = 500, weight=5)

    # --------------------------------------- Title Bar --------------------------------------

    # Assigning properties to the title bar

    title_bar = tk.Frame(
        home_page,
        padx=10,
        pady=20,
        height = 100,
        bg="lightgrey"
    )

    title_label = tk.Label(
        title_bar,
        text="To do list",
        font=TITLE_FONT,
        fg="black",
        bg="lightgrey",
        anchor="w",
        relief="flat",
    )

    # Place title text in the title grid area
    title_label.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    title_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")


    # ------------------------------------- Left side bar ------------------------------------
    left_container = tk.Frame(
        home_page,
        padx=20,
        pady=20,
        bg="white"
    )
    left_container.grid(row=1, column=0, sticky="nsew")

    # Adding a nested grid inside the left container for more of the UI
    left_container.grid_rowconfigure(1, weight=1)
    left_container.grid_columnconfigure(0, weight=1)

    # Button to add a new task, takes user to the page where you enter a new task
    add_task_button = tk.Button(
        left_container,
        text="Add new task",
        command=lambda: switch_page(system_state, "add_task"),
        padx=20,
        pady=20,
        font=("Times New Roman", 18),
        bg = "#2563EB",
        fg = "black",
        relief = "flat",
        activebackground = "#D6D6D6",
        bd = 0,
        cursor = "hand",
        highlightthickness = 0
    )

    add_task_button.grid(row=0, column=0, sticky="nsew")


    # --------------------------------- Scroll bar Container ---------------------------------
    scroll_container = tk.Frame(home_page)
    scroll_container.grid(row=1, column=1, sticky="nsew")

    scroll_container.rowconfigure(0, weight=1)
    scroll_container.columnconfigure(0, weight=1)

    # --------------------------- Scroll bar elements configuration ---------------------------

    # Create a scroll bar container
    canvas = tk.Canvas(scroll_container)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Defining scrolling element
    scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    card_frame = tk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=card_frame, anchor="nw")

    # Define the region
    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    card_frame.bind("<Configure>", update_scrollregion)

    # Make the width the same as its container
    def resize_frame(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_frame)

    # -------------------------------- Scroll bar cards -------------------------------

    # Configure the button on each scroll bar card such that it takes the user to the view task page and displays
    # the correct information that corresponds to the card.

    def open_view_task_page(card_id):
        # store selected task id on the view task page so the information of the current task is accessible
        # from the view task page
        system_state["current_task"] = card_id
        switch_page(system_state, "view_task")

        # Refreshes the text boxes on the add task page so it displays the correct text for the respective task
        system_state["refresh_pages"]["view_task"]()

        # Switches to the view task page
        switch_page(system_state, "view_task")


    # Creates each card with the information from each task
    def create_card(parent, card_id, row):
        card = tk.Frame(
            parent,
            padx=10,
            pady=10,
            highlightbackground="grey",
            highlightthickness=1
        )
        # -------------------------------- Card Layout -------------------------------

        # Nested grid inside each card
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=10)
        card.grid_columnconfigure(2, weight=1)

        # Adding a button to each card, which expands and gives more information about the task
        card_button = tk.Button(
            card,
            text="View task",
            command=lambda: open_view_task_page(card_id),
            padx=5,
            pady=5,
            width=5,
            font=TEXT_FONT,
            bg="#2563EB",
            fg="black",
            relief="flat",
            activebackground="#D6D6D6",
            bd=0,
            cursor="hand",
            highlightthickness = 0
        )

        # Places button inside card grid area
        card_button.grid(row=0, column=2, sticky="ns")

        # Creating the numbers 1, 2, 3 ... at the left end of each card

        card_label = tk.Label(
            card,
            text=card_id+1,
            padx=0,
            pady=5,
            font=TEXT_FONT,
            fg="black",
        )

        card_label.grid(row=0, column=0, sticky="nsew")

        # Display the title of the task on each card

        # title is shortened to fit the frame, there is a max number of characters
        shortened_title = get_shortened_title(card_id)

        card_title = tk.Label(
            card,
            text=shortened_title,
            padx=0,
            pady=5,
            fg="black",
            font = TEXT_FONT,
            anchor="w" # Aligns text to the left
        )

        card_title.grid(row=0, column=1, sticky="nsew")

        # Place the card inside the scrolling frame
        card.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=10,
            pady=5
        )

        parent.grid_columnconfigure(0, weight=1)

    # Creates a card for every to do list item, and also updates it when any changes are made to the list of tasks
    # So that the new cards also show up
    def refresh_home_page_cards():
        for widget in card_frame.winfo_children():
            widget.destroy()

        for i in range(len(task_list)):
            create_card(card_frame, i, i)

    refresh_home_page_cards()

    return home_page, refresh_home_page_cards