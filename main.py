FILE_PATH = "/Users/george/Desktop/Local Files/BDSC/2DIP-AS91896-91897/todolistV1.txt"

def access_tasks():
    with open(FILE_PATH, "r") as file:
        items = file.read().splitlines()
    return items

def print_tasks():
    task_list = access_tasks()
    for i in range(len(task_list)):
        print(f"{i+1}. {task_list[i]} \n")

def mark_as_done():
    task = int(input("Task would you like to mark as done: "))
    with open(FILE_PATH, "r") as file:
        data = file.readlines()
        
    data.pop(task - 1)

    with open(FILE_PATH, "w") as file:
        file.writelines(data)
    

def add_new_task():
    message = input("Description of new task: ")
    with open(FILE_PATH, "a") as file:
        file.write(f"{message}\n")
    
def edit_task():
    task = input("Task would you like to edit: ")
    new_message = input("Enter new task description: ")

    with open(FILE_PATH, "r") as file:
        data = file.readlines()
        
    data[task - 1] = f"{new_message}\n"

    with open(FILE_PATH, "w") as file:
        file.writelines(data)

def main():
    quit = False
    while not quit:
        print("\n \n")
        print("============== To do list ==============")
        print_tasks()
        print("----------------------------------------")
        print("Options: \n 1. Mark task as done \n 2. Add new task \n 3. Edit task \n 4. Quit")
        print("========================================")
        option = int(input("Enter option number: "))

        if option == 1:
            mark_as_done()
        elif option == 2:
            add_new_task()
        elif option == 3:
            edit_task()
        elif option == 4:
            quit = True
        else:
            pass

if __name__ == "__main__":
    main()

    