import json

FILE_PATH = "/Users/george/Desktop/Local Files/BDSC/2DIP-AS91896-91897/todolistV2.txt"

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

task_list = access_tasks()