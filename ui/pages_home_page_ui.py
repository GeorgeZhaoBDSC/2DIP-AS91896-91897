import tkinter as tk
from .backend.to_do_list_functions import *
from .backend.navigation import *
from .backend. refresh import *

def create_home_page(system_state):

    # ============================================= CREATE PAGE =============================================

    # Create root inside the home page function
    root = system_state["root"]
    # Create a home page
    home_page = tk.Frame(root)

    # ============================================= PAGE SETUP =============================================

    def page_setup():
        # Places homepage in the root frame
        home_page.grid(row=0, column=0, sticky="nsew")

        # Expandable window: Top row remains the same width, second row expands, starting at height of 400px
        home_page.rowconfigure(1,minsize = 400, weight=1)

        # The starting width of the window columns is 100/500px, and then expands with the ratio of 1:5
        home_page.columnconfigure(0, minsize = 250, weight=1)
        home_page.columnconfigure(1, minsize = 500, weight=5)


    # ============================================= PAGE CONTENTS =============================================

    # --------------------------------------- Title Bar --------------------------------------
    def create_title_bar():
        # Assigning properties to the title bar
        title_bar = tk.Frame(
            home_page,
            padx=10,
            pady=20,
            height = 100,
            bg="lightgrey"
        )

        title_bar.grid_columnconfigure(0, weight=1)

        title_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

        title_label = tk.Label(
            title_bar,
            text="To do list",
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

    def create_side_bar():
        # ------------------------------------- Side bar setup ------------------------------------
        left_container = tk.Frame(
            home_page,
            padx=20,
            pady=20,
            bg="white",
        )

        # Stops the elements inside left container from changing its width and stretching it
        left_container.grid_propagate(False)

        left_container.grid(row=1, column=0, sticky="nsew")

        # Adding a nested grid inside the left container for more of the UI, configured the rows
        left_container.grid_rowconfigure(0, weight=1)
        left_container.grid_rowconfigure(1, weight=1)
        left_container.grid_rowconfigure(2, weight=3)
        left_container.grid_columnconfigure(0, weight=1)

        # Button to add a new task, takes user to the page where you enter a new task
        add_task_button = tk.Button(
            left_container,
            text="Add new task",
            command=lambda: switch_page(system_state, "add_task"),
            font=("Times New Roman", 18),
            bg = "#2563EB",
            fg = "black",
            relief = "flat",
            activebackground = "#D6D6D6",
            bd = 0,
            cursor = "hand1",
        )
        # ------------------------------------- Add task button ------------------------------------

        # Scroll bar with buttons to switch between lists
        # Padding seperates the add task button from the list buttons
        add_task_button.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # ---------------------------------- List Buttons title ---------------------------------

        # Created a label for the list buttons below
        list_title = tk.Label(
            left_container,
            text="To Do Lists:",
            font=("Times New Roman", 18),
            fg="black",
            bg="white",
            relief="flat",
            anchor="center",
            justify="center"
        )

        list_title.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10,
        )

        # ------------------------------------- List Buttons ------------------------------------

        # Create container for the buttons
        list_btn_container = tk.Frame(left_container)

        # Resize the grid areas
        list_btn_container.rowconfigure(0, weight=1)
        list_btn_container.columnconfigure(0, weight=1)

        list_btn_container.grid(row=2, column=0, sticky="nsew")

        btn_canvas = tk.Canvas(list_btn_container, bg="white", highlightthickness=0)
        btn_scrollbar = tk.Scrollbar(
            list_btn_container,
            orient="vertical",
            command=btn_canvas.yview
        )

        # Create scroll bar
        btn_canvas.configure(yscrollcommand=btn_scrollbar.set)

        # Assign areas for the buttons and scroll bar
        btn_canvas.grid(row=0, column=0, sticky="nsew")
        btn_scrollbar.grid(row=0, column=1, sticky="ns")

        # Create the frame to put the buttons of the scroll bar in
        btn_frame = tk.Frame(btn_canvas)
        btn_window = btn_canvas.create_window((0, 0), window=btn_frame, anchor="nw")
        btn_frame.grid_columnconfigure(0, weight=1)

        def update_btn_scrollregion(event):
            btn_canvas.configure(scrollregion=btn_canvas.bbox("all"))

        def resize_btn_frame(event):
            btn_canvas.itemconfig(btn_window, width=event.width)

        # Configure the regions to update when scrolling
        btn_frame.bind("<Configure>", update_btn_scrollregion)
        btn_canvas.bind("<Configure>", resize_btn_frame)

        def switch_list(list_id):
            system_state["current_task"][0] = list_id
            system_state["refresh_pages"]["home"]()

        # Create the button for each list
        def create_button(list_id):
            # Title of the button is the title of the To do list
            button_text = list(task_list.keys())[list_id]

            # Style for the button
            button = tk.Button(
                btn_frame,
                text=button_text,
                command=lambda: switch_list(list_id),
                padx=10,
                pady=10,
                font=TEXT_FONT,
                bg="lightgrey",
                fg="black",
                relief="flat",
                activebackground="#D6D6D6",
                bd=0,
                cursor="hand1",
            )

            button.grid(row=list_id, column=0, sticky="nsew", pady=5)

        # Creates all of the buttons
        for i in range(len(task_list)):
            create_button(i)

    # --------------------------------- Tasks cards (right side) ---------------------------------

    def create_task_cards():
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

        def open_view_task_page(task_id):
            # store selected task id on the view task page so the information of the current task is accessible
            # from the view task page
            system_state["current_task"] = task_id
            switch_page(system_state, "view_task")

            # Refreshes the text boxes on the add task page so it displays the correct text for the respective task
            system_state["refresh_pages"]["view_task"]()

            # Switches to the view task page
            switch_page(system_state, "view_task")


        # Creates each card with the information from each task
        def create_card(parent, task_id):

            # Colour the border of each card depending on the importance of the card
            # create a dictionary that maps the importance to the respective colour
            colour_map = dict(zip(PRIORITY_OPTIONS, PRIORITY_COLOURS))

            highlight_colour = colour_map[list(task_list.values())[task_id[0]][task_id[1]]["priority"]]

            card = tk.Frame(
                parent,
                padx=10,
                pady=10,
                highlightbackground=highlight_colour,
                highlightthickness=2,
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
                command=lambda: open_view_task_page(task_id),
                padx=5,
                pady=5,
                width=5,
                font=TEXT_FONT,
                bg="#2563EB",
                fg="black",
                relief="flat",
                activebackground="#D6D6D6",
                bd=0,
                cursor="hand1",
                highlightthickness = 0
            )

            # Places button inside card grid area
            card_button.grid(row=0, column=2, sticky="ns")

            # Creating the numbers 1, 2, 3 ... at the left end of each card

            card_label = tk.Label(
                card,
                text=task_id[1]+1,
                padx=0,
                pady=5,
                font=TEXT_FONT,
                fg="black",
            )

            card_label.grid(row=0, column=0, sticky="nsew")

            # Display the title of the task on each card

            # title is shortened to fit the frame, there is a max number of characters
            shortened_title = get_shortened_title(task_id)

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
                row=task_id[1],
                column=0,
                sticky="ew",
                padx=10,
                pady=5
            )

            parent.grid_columnconfigure(0, weight=1)


        # Creates a card for every to do list item in the current to do list, which is list number task_id[0]
        task_id = system_state["current_task"]
        for i in range(len(list(task_list.values())[task_id[0]])):
            create_card(card_frame, [task_id[0], i])

    # ====================================== COMPILE FUNCTIONS & LOAD PAGE ======================================

    def build_page():
        create_title_bar()
        create_side_bar()
        create_task_cards()

    def refresh_home():
        refresh(home_page, build_page)

    page_setup()
    build_page()

    return home_page, refresh_home


