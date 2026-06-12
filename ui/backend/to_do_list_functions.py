import json

# The maximum number of characters of the title to a task displayed on each card on the home page
TITLE_LENGTH = 50

# Default font for title and regular text
TITLE_FONT = ("Times New Roman", 50)

TEXT_FONT = ("Times New Roman", 12)

# Options for priority selection for the tasks
PRIORITY_OPTIONS = ("High Importance", "Medium Importance", "Low Importance", "COMPLETE")

# Colour (border of the cards on the home page) for each priority
PRIORITY_COLOURS = ("red", "orange", "yellow", "green")

FILE_PATH = "ui/backend/tasks.json"

def access_tasks():
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def save_tasks():
    with open(FILE_PATH, "w") as file:
        json.dump(task_list, file)

def add_new_task(title, description, priority, date):
    task_list.append({"title": title, "description": description, "priority": priority, "date": date})
    # Sort the tasks in order of priority/date
    sort_tasks()
    save_tasks()

def edit_task(task_id, title, description, priority, date):
    task_list[task_id] = {"title": title, "description": description, "priority": priority, "date": date}
    save_tasks()

def delete_task(task_id):
    del task_list[task_id]
    save_tasks()

def get_task_info(task_id):
    return task_list[task_id]

def get_shortened_title(task_id):
    # Get the title for the task and shorten it to at most TITLE_LENGTH
    title = task_list[task_id]["title"]
    shortened_title = title[:TITLE_LENGTH]
    return shortened_title

def sort_tasks():
    # Create a dictionary that converts between the priority options and their order in numbers (0, 1, 2...)
    priority_map = {PRIORITY_OPTIONS[i]:i for i in range(len(PRIORITY_OPTIONS))}

    # Sorts the task list. First based on priority, then within the same priority, sort by due date
    task_list.sort(
        key=lambda task: (
            priority_map[task["priority"]],
            task["date"]
        )
    )

task_list = access_tasks()