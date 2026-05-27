import json

# The maximum number of characters of the title to a task displayed on each card on the home page
TITLE_LENGTH = 50

TITLE_FONT = ("Times New Roman", 50)

TEXT_FONT = ("Times New Roman", 12)

PRIORITY_OPTIONS = ("Very improtnat", "kinda improtnat", "nahh")

FILE_PATH = "/Users/george/PycharmProjects/PythonProject/2DIP_Internal/Version3/ui/backend/tasks.json"

def access_tasks():
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def save_tasks():
    with open(FILE_PATH, "w") as file:
        json.dump(task_list, file)

def add_new_task(title, description):
    task_list.append({"title": title, "description": description})
    save_tasks()

def edit_task(task_id, title, description):
    task_list[task_id] = {"title": title, "description": description}
    save_tasks()

def delete_task(task_id):
    del task_list[task_id]
    save_tasks()

def get_task_info(task_id):
    return task_list[task_id]

def get_shortened_title(task_id):
    title = task_list[task_id]["title"]
    shortened_title = title[:TITLE_LENGTH]
    return shortened_title

task_list = access_tasks()