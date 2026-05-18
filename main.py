import tkinter as tk
from backend import *

# ------------------------------------- Create Root ------------------------------------
root = tk.Tk()

# Make root expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Basic text font for the app
TEXT_FONT = ("Times New Roman", 12)

# ------------------------------- Navigating between pages  -----------------------------

def switch_page(page):
    page.tkraise()

#####################################################################################################################
##################################################### HOME PAGE #####################################################
#####################################################################################################################

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

title_label = tk.Label(
    home_page,
    text="Title",
    padx=10,
    pady=10,
    font=("Times New Roman", 50),
    fg="white",
    bg="blue"
)

title_label.grid(row=0, column=0, columnspan=2, sticky="nsew")


# ------------------------------------- Left side bar ------------------------------------
left_container = tk.Frame(
    home_page,
    padx=20,
    pady=20,
    bg="yellow"
)
left_container.grid(row=1, column=0, sticky="nsew")

# Adding a nested grid inside the left container for more of the UI
left_container.grid_rowconfigure(1, weight=1)
left_container.grid_columnconfigure(0, weight=1)

# Button to add a new task, takes user to the page where you enter a new task
add_task_button = tk.Button(
    left_container,
    text="Add new task",
    command=lambda: switch_page(add_task_page),
    padx=20,
    pady=20,
    font=("Times New Roman", 18),
    bg="white",
    fg="black"
)

add_task_button.grid(row=0, column=0, sticky="nsew")


# --------------------------------- Scroll bar Container ---------------------------------
scroll_container = tk.Frame(home_page)
scroll_container.grid(row=1, column=1, sticky="nsew")

scroll_container.rowconfigure(0, weight=1)
scroll_container.columnconfigure(0, weight=1)

# --------------------------- Scroll bar elements configuration ---------------------------
canvas = tk.Canvas(scroll_container)
canvas.grid(row=0, column=0, sticky="nsew")

# --- SCROLLBAR ---
scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)

# --- FRAME INSIDE CANVAS ---
card_frame = tk.Frame(canvas)
window_id = canvas.create_window((0, 0), window=card_frame, anchor="nw")

# --- SCROLL REGION UPDATE ---
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

card_frame.bind("<Configure>", update_scrollregion)

# --- KEEP WIDTH MATCHED ---
def resize_frame(event):
    canvas.itemconfig(window_id, width=event.width)

canvas.bind("<Configure>", resize_frame)

# -------------------------------- Scroll bar cards -------------------------------

# Configure the button on each scroll bar card such that it takes the user to the view task page and displays
# the correct information that corresponds to the card.

def open_view_task_page(card_id):
    task = task_list[card_id]

    # Clears the title and description entry boxes on the view task page
    title_edit_entry.delete("1.0", tk.END)
    description_edit_entry.delete("1.0", tk.END)

    # Writes new title and description into those 2 entry boxes on the view task page
    title_edit_entry.insert("1.0", task["title"])
    description_edit_entry.insert("1.0", task["description"])

    # store selected task id on the view task page
    view_task_page.current_task_id = card_id

    # Switches to the view task page
    switch_page(view_task_page)


# Creates each card with the information from each task
def create_card(parent, card_id, row):
    card = tk.Frame(
        parent,
        padx=10,
        pady=10,
        relief="ridge",
        bd = 2
    )
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
        font=("Times New Roman", 12),
        bg="white",
        fg="black"
    )

    # Places button inside card grid area
    card_button.grid(row=0, column=2, sticky="ns")

    # Creating the numbers 1, 2, 3 ... at the left end of each card

    card_label = tk.Label(
        card,
        text=card_id+1,
        padx=0,
        pady=5,
        font=("Times New Roman", 20),
        fg="black",
    )

    card_label.grid(row=0, column=0, sticky="nsew")

    # Place the card inside the scrolling frame
    card.grid(
        row=row,
        column=0,
        sticky="ew",
        padx=10,
        pady=5
    )

    #
    parent.grid_columnconfigure(0, weight=1)

# Creates a card for every to do list item, and also updates it when any changes are made to the list of tasks
# So that the new cards also show up
def refresh_home_page_cards():
    for widget in card_frame.winfo_children():
        widget.destroy()

    for i in range(len(task_list)):
        create_card(card_frame, i, i)

refresh_home_page_cards()

#####################################################################################################################
################################################### ADD TASK PAGE ###################################################
#####################################################################################################################

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
    text="Title",
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
    title = title_entry.get()
    description = description_entry.get()

    # Adds the new task to the list of tasks and also saves it to the json file
    add_new_task(title, description)

    # Refreshes the home page so that the new cards show up on the home page
    refresh_home_page_cards()

    # Clear everything entered in those 2 fields
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

# Create a label for the entry box where the user enters the title of the new task
title_label = tk.Label(
    add_task_page,
    text="Title: ",
    padx=20,
    pady=10,
    font=TEXT_FONT,
)

# Create entry box where the user enters the title of the new task
title_entry = tk.Entry(
    add_task_page,
    font=TEXT_FONT,
)

# Create a label for the entry box where the user enters the description of the new task
description_label = tk.Label(
    add_task_page,
    text="Description:",
    padx=20,
    pady=10,
    font=TEXT_FONT,
)

# Create the entry box where the user enters the description of the new task
description_entry = tk.Entry(
    add_task_page,
    font=TEXT_FONT,
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
    font=TEXT_FONT,
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
    command=lambda: switch_page(home_page),
    font=TEXT_FONT,
    bg="green",
    fg="black",
    padx = 10,
    pady = 10,
)

exit_button.grid(row=3, column=0)

#####################################################################################################################
################################################### VIEW TASK PAGE ##################################################
#####################################################################################################################

# ----------------------------------- General Page setup ---------------------------------
# Create a add task page
view_task_page = tk.Frame(root)

view_task_page.current_task_id = None

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
    text="Title",
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
    font=TEXT_FONT,
)

# Create test box where the user can edit the task title
title_edit_entry = tk.Text(
    view_task_page,
    font=TEXT_FONT,
    height=2
)

# Create a label for the entry box where the user enters the description of the new task
description_edit_label = tk.Label(
    view_task_page,
    text="Description:",
    padx=20,
    pady=10,
    font=TEXT_FONT,
)

# Create the entry box where the user enters the description of the new task
description_edit_entry = tk.Text(
    view_task_page,
    font=TEXT_FONT,
    height=12
)

# Makes both text boxes sticky left to right, however title text box doesn't have to be very wide
# so it is not sticky top to bottom like the description entry box
title_edit_label.grid(row=1, column=0, sticky="ew")
title_edit_entry.grid(row=1, column=1, columnspan=2, sticky="ew")

description_edit_label.grid(row=2, column=0, sticky="ew")
description_edit_entry.grid(row=2, column=1, columnspan=2, sticky="ew")

# Add the information about the current task for the user to view and edit from the View Task button on the home page

# --------------------------------------- Save button --------------------------------------
# Save the information about the task that the user changed
def save_task_info():
    task_id = view_task_page.current_task_id
    updated_title = title_edit_entry.get("1.0", "end-1c")
    updated_description = description_edit_entry.get("1.0", "end-1c")

    edit_task(task_id, updated_title, updated_description)

    # Refresh the home page card scroll bar so update shows up
    refresh_home_page_cards()


# Button that saves the entry the user has edited
save_button = tk.Button(
    view_task_page,
    text="Save Changes",
    command=lambda: save_task_info(),
    font=TEXT_FONT,
    bg="green",
    fg="black",
    padx = 15,
    pady = 10,
)

save_button.grid(row=3, column=2)

# --------------------------------------- Delete button --------------------------------------
# Deletes the task and clears entry box
def delete_task_info():
    task_id = view_task_page.current_task_id
    title_edit_entry.delete("1.0", tk.END)
    description_edit_entry.delete("1.0", tk.END)

    # Deletes the task from the list of tasks and json file
    delete_task(task_id)

    # Refresh the home page card scroll bar so update shows up
    refresh_home_page_cards()

# Button that saves the entry the user has edited
delete_button = tk.Button(
    view_task_page,
    text="Delete task",
    command=lambda: delete_task_info(),
    font=TEXT_FONT,
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
    command=lambda: switch_page(home_page),
    font=TEXT_FONT,
    bg="green",
    fg="black",
    padx = 10,
    pady = 10,
)

exit_button.grid(row=3, column=0)

# Display home page
home_page.tkraise()

root.mainloop()