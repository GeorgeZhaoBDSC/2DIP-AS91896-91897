import json

# The maximum number of characters of the title to a task displayed on each card on the home page
TITLE_LENGTH = 50

# Default font for title and regular text
TITLE_FONT = ("Times New Roman", 50)

TEXT_FONT = ("Times New Roman", 12)

# Options for priority selection for the tasks
PRIORITY_OPTIONS = ("High Importance", "Medium Importance", "Low Importance")

# Colour (border of the cards on the home page) for each priority
PRIORITY_COLOURS = ("red", "yellow", "green")

FILE_PATH = "ui/backend/tasks.json"

def access_tasks():
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def save_tasks():
    with open(FILE_PATH, "w") as file:
        json.dump(task_list, file)

def add_new_task(title, description, priority, date, list_number):
    task_list[list(task_list.keys())[list_number]].append({"title": title, "description": description, "priority": priority, "date": date})
    # Sort the tasks in order of priority/date
    sort_tasks()
    save_tasks()

def edit_task(task_id, title, description, priority, date):
    task_list[list(task_list.keys())[task_id[0]]][task_id[1]] = {"title": title, "description": description, "priority": priority, "date": date}
    # Sort the tasks in order of priority/date
    save_tasks()

def delete_task(task_id):
    del task_list[list(task_list.keys())[task_id[0]]][task_id[1]]
    save_tasks()

def mark_as_done(task_id):
    # Delete the task from its current list
    task_info = task_list[list(task_list.keys())[task_id[0]]].pop(task_id[1])
    # Adds it to the finished list
    task_list[list(task_list.keys())[-1]].append(task_info)
    # Sort & Save the list
    sort_tasks()
    save_tasks()

def get_task_info(task_id):
    return list(task_list.values())[task_id[0]][task_id[1]]

def get_shortened_title(task_id):
    # Get the title for the task and shorten it to at most TITLE_LENGTH
    title = list(task_list.values())[task_id[0]][task_id[1]]["title"]
    shortened_title = title[:TITLE_LENGTH]
    return shortened_title

def sort_tasks():
    # Create a dictionary that converts between the priority options and their order in numbers (0, 1, 2...)
    priority_map = {PRIORITY_OPTIONS[i]:i for i in range(len(PRIORITY_OPTIONS))}

    # Sorts each task list. First based on priority, then within the same priority, sort by due date
    for i in range(len(task_list)):
        task_list[list(task_list.keys())[i]].sort(
            key=lambda task: (
                priority_map[task["priority"]],
                task["date"]
            )
        )

def create_new_list():
    list_names = list(task_list.keys())

    # Choose a name for the new list that is not the same as one of the previous ones.
    # Loop through the numbers after the "Untitled List" until one is found not to be the same.
    naming_index = 1
    list_name = "Untitled List " + str(naming_index)

    while list_name in list_names:
        naming_index += 1
        list_name = "Untitled List " + str(naming_index)

    # Add the new list with its name to the task list, at the second to last position
    # Since the last position is always reserved for the COMPLETED list
    new_task_list = {}

    final_element = list(task_list.keys())[-1]

    for key, value in task_list.items():
        if key == final_element:
            new_task_list[list_name] = []
        new_task_list[key] = value

    task_list.clear()
    task_list.update(new_task_list)

    # Save task list
    save_tasks()

def delete_list(list_id):
    # Find the name of the list
    list_name = list(task_list.keys())[list_id]

    # Delete list
    del task_list[list_name]

    # Save task list
    save_tasks()

task_list = access_tasks()