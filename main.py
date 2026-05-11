# Assign the file that stores the to do list information
FILE_PATH = "/Users/george/Desktop/Local Files/BDSC/2DIP-AS91896-91897/todolistV1.txt"

def access_tasks():
    # Open the file that stores the to do list, access the information and put it in a list
    with open(FILE_PATH, "r") as file:
        items = file.read().splitlines()
    return items

def print_tasks():
    # Print the list of tasks on the text UI
    task_list = access_tasks()
    for i in range(len(task_list)):
        print(f"{i+1}. {task_list[i]} \n")

def mark_as_done():
    # Get the user to input which task they would like to mark as done
    task = int(input("Task would you like to mark as done: "))
    with open(FILE_PATH, "r") as file:
        data = file.readlines()
    
    # Delete the task from the list, and saving to the txt file
    data.pop(task - 1)

    with open(FILE_PATH, "w") as file:
        file.writelines(data)
    

def add_new_task():
    # Get user input for the description of the new task, then add it to the txt file
    message = input("Description of new task: ")
    with open(FILE_PATH, "a") as file:
        file.write(f"{message}\n")
    
def edit_task():
    # Get the user to input the task they would like to edit, then the new description for the task
    task = int(input("Task would you like to edit: "))
    new_message = input("Enter new task description: ")

    # Open the file and update the edited task
    with open(FILE_PATH, "r") as file:
        data = file.readlines()
        3
    data[task - 1] = f"{new_message}\n"

    with open(FILE_PATH, "w") as file:
        file.writelines(data)

def main():
    # Main loop
    quit = False
    while not quit:
        # Print out to-do list in a clean and organised style using spacing and new lines
        print("\n \n")
        print("============== To do list ==============")
        print_tasks()
        print("----------------------------------------")
        print("Options: \n 1. Mark task as done \n 2. Add new task \n 3. Edit task \n 4. Quit")
        print("========================================")
        option = int(input("Enter option number: "))

        # Asks the user for the action they want to do, then mapping it to the respective functions

        if option == 1:
            mark_as_done()
        elif option == 2:
            add_new_task()
        elif option == 3:
            edit_task()
        elif option == 4:
            quit = True
            # Quit the program by stopping the while loop
        else:
            pass

if __name__ == "__main__":
    main()

    