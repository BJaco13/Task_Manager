#===== Importing Libraries =====
from datetime import datetime

#===== Functions Section =====

def main_menu(username, all_users, all_tasks, total_num_of_tasks):

    while True:
        menu = ""
        # Presenting the menu to the user and making sure that the user input is converted to lower case.
        if username != 'admin':
            menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

        elif username == 'admin':
            # Adding a special option for the admin of the program to be able to see statistics.
            # Only the admin is allowed to view the statistics so it's only made availble to him
            menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
s - View Statistics
gr - Generate Reports
e - Exit
: ''').lower()

        if menu == 'r' and username == 'admin':
            # If the user selects 'r' and the user is the admin, then only are they allowed to use this section.
            reg_user(all_users)

        elif menu == 'r' and username != 'admin':
            # Display an error message if the user does not  have permission to add any users
            print("\nYou unfortunately do not have access to add users.\n")

        elif menu == 's':
            # This is the statistics option. Shows the total amount of users and task currently active.

            print('''\nWelcome to your statistics panel:
Total number of users:\t\t{}
Total number of tasks:\t\t{}\n'''.format(len(all_users), total_num_of_tasks))

        elif menu == 'a':
            # This section allows the user to add new tasks to the tasks.txt file
            add_task(all_users)

        elif menu == 'va':
            # This section shows all the tasks currently logged in the tasks.txt
            view_all()

        elif menu == 'vm':
            # This section shows the user all the tasks currently assigned to their username
            view_mine()
    
        elif menu == 'gr':
            # This section will generate certian reports for the admin user

            # Task Overview Section and User Overview Section  . Call these functions to write and update the files
            task_overview(all_tasks)
            user_overview(all_tasks, all_users)

            # Extract the data from the files and print out
            # First declare variables and lists to use in this section
            task_overview_list = []
            user_overview_list = []

            # Write task_overview.txt file to a list
            f = open('task_overview.txt', 'r')
            for line in f:
                line = line.strip('\n')
                line = line.split(', ')
                task_overview_list.append(line)
            f.close()

            # Write user_overview.txt file to a list
            f = open('user_overview.txt', 'r')
            x = 1
            for line in f:
            
                # Use the If Loop to save the first line of the file into a seperate list which shows general data
                # The rest of the file will contain the specified data for each user
                if x == 1:
                    first_line = line.strip('\n')
                    first_line = line.split(', ')
                else:
                    line = line.strip('\n')
                    line = line.split(', ')
                    user_overview_list.append(line)  
                x +=1
            f.close()

            # Print out the task_overview file data
            print("""\n\t\tTask Overview:

Total tasks generated and tracked in app: {}
Total number of completed tasks: {}
Total number of uncompleted tasks: {}
Percentage of incompleted tasks: {}
Total number of tasks that are overdue and incompleted: {}
Percentage of tasks that are overdue: {}
""".format(task_overview_list[0][0], task_overview_list[0][1], task_overview_list[0][2], task_overview_list[0][3], task_overview_list[0][4], task_overview_list[0][5]))


            # Print out the user_overview file data starting with the general data and then user specific data
            print("""\n\t\tUser Overview:

Total number of users registered: {}
Total number of tasks generated and tracked in the app: {}""".format(first_line[0], first_line[1]))


            # Use For Loop to run through the list and print out all the data
            for x in range(0, len(user_overview_list)):
            
                print("""Statistics for user: {}
Total number of tasks assigned: {}
Percentage of tasks assigned: {}
Percentage of tasks assigned that are completed: {}
Percentage of tasks assigned that are not completed yet: {}
Percentage of tasks assigned that are not completed yet and overdue: {}
""".format(user_overview_list[x][0], user_overview_list[x][1], user_overview_list[x][2], user_overview_list[x][3], user_overview_list[x][4], user_overview_list[x][5]))

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice. Please try again")

def reg_user(all_users_dict):
    # Ask the user to enter a new username and password and register a new user
    
    # Check if the username entered already exists  . If it does, program will prompt to try again
    new_user_valid = False
    while new_user_valid == False:
        new_user = input("Please enter the new username: ")

        if new_user in all_users_dict:
            print("\nThis user already exists. Please make sure to enter a different username.\n") 
        else:
            new_user_valid == True
            break    

    # Checking if the new password is valid  . 
    # While it's false, ask the user to enter until new_pass and confirm_new_pass are the same
    new_pass_valid = False
    while new_pass_valid == False:

        new_pass = input("Please enter the password for the user: ")
        confirm_new_pass = input("Please enter password again to confirm: ")

        if new_pass == confirm_new_pass:
            new_pass_valid == True
            break
        else:
            print("\nThere is an inconsistency between the two passwords entered. Please try again.\n")
            pass
        
    # Write the newly, validated user info into the user.txt file
    try:

        f = open('user.txt', 'r+')
        previous_content = f.read()
        f.write("\n{}, {}".format(new_user, new_pass))
        f.close()
    
    except FileNotFoundError:
        print("There has been an error in trying to register the user. Check reg_user function.")

    print("\nThe user {} has been successfully added!\n".format(new_user))

def add_task(all_users):
    # Ask the user for all the task info needed, then once done, write to the file tasks.txt
    # Add a while not loop to make sure user that is entered is a user that exists within the data files
    a_user = ""
    while a_user not in all_users:
        a_user = input("Please enter the user you would like to assign the task to: ")
    a_task_title = input("Please enter a title: ")
    a_description = input("Please enter a description: ")
    a_due_date = input("Please enter a due date in the format as the example '10 Oct 2019': ")

    # Checked how to get the current date by importing datetime. Function is datetime.now() and 
    # use the strftime() for formatting the date
    # https://www.programiz.com/python-programming/datetime/strftime
    current_date = datetime.now().strftime("%d %b %Y")
    task_completed = "No"

    # Here we write the task to the file called tasks.txt
    # Use a try-catch block to make sure that it writes to the file
    try:

        f = open('tasks.txt', 'r+')
        previous_content = f.read()
        f.write("\n{}, {}, {}, {}, {}, {}".format(a_user, a_task_title, a_description, current_date, a_due_date, task_completed))
        print("\nTask has been successfully added!\n")
        f.close()
    
    except FileNotFoundError:
        print("The file was not found to add the task to. Check add_task function.")

def view_all():
# Read the tasks.txt file to display all tasks to the user

    # Use a try-catch block to make sure the file opens
    try:

        f = open('tasks.txt', 'r')

        for line in f:
            task_for_user = line.split(", ")

            # Read the tasks.txt file and display all the tasks
            print("\nTask:\t\t\t{}".format(task_for_user[1]))
            print("Assigned to:\t\t{}".format(task_for_user[0]))
            print("Date Assigned:\t\t{}".format(task_for_user[3]))
            print("Due Date:\t\t{}".format(task_for_user[4]))
            print("Task Complete?\t\t{}".format(task_for_user[5].strip("\n")))
            print("Task Description:\n{}".format(task_for_user[2]))
            print("\n")
        f.close()

    except FileNotFoundError:
        print("An error has occured in trying to view all the tasks. Check the view_all function.")

def view_mine():
# Read the tasks.txt file and display only tasks that are assigned to the currently logged in user
    while True:
        users_tasks_dict = {}
        counter = 1
        task_for_user = []

        try:
            f = open('tasks.txt', 'r')

            for line in f:
                task_for_user = line.split(", ")

                # Prints out each task in a good display
                if task_for_user[0] == username:
                    print("\nTask number: {}".format(counter))
                    print("Task:\t\t\t{}".format(task_for_user[1]))
                    print("Assigned to:\t\t{}".format(task_for_user[0]))
                    print("Date Assigned:\t\t{}".format(task_for_user[3]))
                    print("Due Date:\t\t{}".format(task_for_user[4]))
                    print("Task Complete?\t\t{}".format(task_for_user[5].strip("\n")))
                    print("Task Description:\n{}".format(task_for_user[2]))
                    print("\n")

                    # Create a dictionary to access and diplay tasks numerically.
                    # Add each task in the list task_for_user into the dictionary, each assigned its own key
                    users_tasks_dict[counter] = task_for_user
                    counter +=1
                else:
                    pass
            f.close()

        except FileNotFoundError:
            print("A problem has occured in displaying the tasks. Check the view_mine function.")

        # Ask the user which tasks they want to select, then ask the appropriate questions regarding the task

        # Use While Loop to check that input is a didgit then cast to an int variable
        va_first_menu = ""
        while va_first_menu.isdigit() == False:
            va_first_menu = input("""* Please enter the task number of the task that you want to select
* To return to the previous menu enter '-1'
:""")
            if va_first_menu == '-1':
                main_menu(username, all_users, all_tasks, total_num_of_tasks)

        va_first_menu = int(va_first_menu)

        if va_first_menu in users_tasks_dict:
            
            # Use While Loop to check that input is a didgit then cast to an int variable
            va_second_menu = ""
            while va_second_menu.isdigit() == False:
                va_second_menu = input("""Please select an option below: 
1. Mark the task as complete
2. Edit the task
:""")

            va_second_menu = int(va_second_menu)

            if va_second_menu == 1:
                # This option will change the task complete status to 'Yes' to show it's been completed

                # Change the 'No' to a 'Yes' by inserting a yes in the index of the no  . Send to function update_tasks
                users_tasks_dict[va_first_menu][5] = 'Yes'
                update_tasks(users_tasks_dict)
                print("\nThe task has been marked as complete!\n")

            elif va_second_menu == 2 and task_for_user[5].strip("\n") == 'No':
                # This option allows the user to edit the task selected  . Specifically the user assigned or due date

                # Use While Loop to check if the input is a digit then cast input to int once it's true
                task_edit_option = ""
                while task_edit_option.isdigit() == False:
                    task_edit_option = input("""Please select an option below:
1. Edit the user this task is assigned to
2. Edit the due date of this task 
:""")
                task_edit_option = int(task_edit_option)

                if task_edit_option == 1:
                    # This option is available to change the user that this task is assigned to

                    # Get new user info, change in dictionary and send to funtion update_tasks
                    change_user = input("Please insert the new user you would like to assign this task to: ")
                    users_tasks_dict[va_first_menu][0] = change_user
                    update_tasks(users_tasks_dict)
                    print("\nThe user has been successfully changed!\n")

                elif task_edit_option == 2:
                    # This option is available to change the due date of this task

                    # Get due date info, change in dictionary and send to funtion update_tasks
                    change_due_date = input("Please insert the due date you would like to assign this task to: ")
                    users_tasks_dict[va_first_menu][4] = change_due_date
                    update_tasks(users_tasks_dict)
                    print("\nThe due date has been successfully changed!\n")
                
                else:
                    print("Please enter a valid task number.")

            elif va_second_menu == 2 and task_for_user[5].strip("\n") == 'Yes':
                # This simply gives an error message to say the task cannot be edited due to completion status = Yes
                print("Sorry, this task has already been marked complete. Therefore no more changes can be made.")

            else:
                print("Please enter a valid task number.")

        else:
            print("Please make sure you select one of the displayed task numbers.")

def update_tasks(users_tasks_dict):
    try:
        # Write to tasks.txt file the new status of the task
        f = open('tasks.txt', 'r')

        # Read all tasks and add updates to relevant tasks and save in dictionary called all_users_tasks_dict
        counter = 1
        all_users_tasks_dict = {}
        for line in f:
            all_users_tasks_dict[counter] = line.strip('\n').split(', ')
            counter +=1
        f.close()
    
    except FileNotFoundError:
        print("An error has occured in trying to open the data file. Check update_tasks function.")

    # Use the first level For Loop to run the total amount of entries in all_users_tasks
    # Second level For Loop runs the total amount of entries in the users_tasks_dict
    # Then it loops through the lists and compares all the data, and if the whole list is the same, it'll overwrite
    # to be sure that if anything changed it'll update accordingly
    # it also slices the info to just check the similarities of the task tile, description and date it's been created
    for x in range(0, len(users_tasks_dict)):

        for y in range(0, len(all_users_tasks_dict)):

            if all_users_tasks_dict[y+1][1:4] == users_tasks_dict[x+1][1:4]:

                all_users_tasks_dict.update({y+1: users_tasks_dict[x+1]})
                
    try:
        # Use write_line variable to print each value of every key in the dictionary
        # Then use the variable write_line and write it to the tasks.txt file
        f = open('tasks.txt', 'w')
        for key in all_users_tasks_dict:
            write_line = all_users_tasks_dict[key]
            f.write(", ".join(write_line) + "\n")
        f.close()
    
    except FileNotFoundError:
        print("An error has occured i ntrying to open the data file. Check update_tasks function.")

def task_overview(all_tasks):

    # Declare the variables for calculations to follow
    total_tasks_completed = 0
    current_date = datetime.now().strftime("%d %b %Y")
    tasks_overdue = 0
    tasks_overdue_and_incomplete = 0
    total_tasks_incomplete = 0

    # For Loop to calculate certain variables for calculations
    for line in all_tasks:
        line = line.split(', ')

        # Caculate amount of tasks overdue and incomplete
        if line[5].strip('\n') == 'No' and line[4] < current_date:
            tasks_overdue_and_incomplete+=1

        # Calculate the amount of tasks completed
        if line[5].strip('\n') == 'Yes':
            total_tasks_completed +=1
            
        # Calculate the amount of incomplete tasks
        if line[5].strip('\n') == 'No':
            total_tasks_incomplete +=1

        # Calculate the amount of tasks overdue
        if line[4] < current_date:
            tasks_overdue +=1
            
    # Calculate the percentage of incomplete tasks and tasks overdue
    percent_tasks_incomplete = (total_tasks_incomplete / len(all_tasks)) * 100
    percentage_tasks_overdue = (tasks_overdue_and_incomplete / len(all_tasks)) * 100

    try:
        # Write all the data to the file task_overview.txt
        f = open('task_overview.txt', 'w+')
        f.write("{}, {}, {}, {}, {}, {}\n".format(len(all_tasks), total_tasks_completed, total_tasks_incomplete, tasks_overdue_and_incomplete, percent_tasks_incomplete, percentage_tasks_overdue))
        f.close()

    except FileNotFoundError:
        print("An error has occured with opening the file. Check the task_overview function.")

def user_overview(all_tasks, all_users):

    # Declare the variables used for calculations in this section
    tasks_amount = len(all_tasks)
    users_amount = len(all_users)
    current_date = datetime.now().strftime("%d %b %Y")
    user_overview_list = []
    user_overview_list_general = []
    
    # Use For Loop to run through all users
    for user in all_users:
    
        # Declare all varaibles being used in this section
        amount_tasks_for_curr_user = 0
        percent_tasks_assigned_to_curr_user = 0.0

        amount_tasks_compl_curr_user = 0
        percent_tasks_compl_curr_user = 0.0
        percent_tasks_not_compl_curr_user = 0.0

        amount_tasks_overdue_not_compl = 0
        percent_tasks_overdue_not_compl = 0.0

        # Use the second For Loop to run through all the tasks
        for line in all_tasks:
            line = line.split(', ')

            # Use the If Loop to only proceed if the tasks is assigned to the currently selected user
            if user == line[0]:
                amount_tasks_for_curr_user +=1
                
                # Checks if the completion status is true and if so, adds one to variable task completed
                if line[5].strip('\n') == 'Yes':
                    amount_tasks_compl_curr_user +=1
                
                # Checks if the completion status is true and duedate of task
                if line[5].strip('\n') == 'No' and line[4] < current_date:
                    amount_tasks_overdue_not_compl +=1
        
        percent_tasks_assigned_to_curr_user = (amount_tasks_for_curr_user / len(all_tasks)) * 100

        # Using an If Loop to make sure I don't divide with a 0  . If it's a zero, set percentages accordingly
        # This will only happen when there has been no tasks assigned to a user
        if amount_tasks_for_curr_user != 0:
            percent_tasks_compl_curr_user = round((amount_tasks_compl_curr_user / amount_tasks_for_curr_user) * 100, 2)
            percent_tasks_not_compl_curr_user = round(100 - percent_tasks_compl_curr_user, 2)
            percent_tasks_overdue_not_compl = round((amount_tasks_overdue_not_compl / amount_tasks_for_curr_user) * 100, 2)
        
        else:
            percent_tasks_compl_curr_user = 0.0
            percent_tasks_not_compl_curr_user = 0.0
            percent_tasks_overdue_not_compl = 0.0

        user_overview_list.append("{}, {}, {}, {}, {}, {}\n".format(user, amount_tasks_for_curr_user, percent_tasks_assigned_to_curr_user, percent_tasks_compl_curr_user, percent_tasks_not_compl_curr_user, percent_tasks_overdue_not_compl))

    user_overview_list_general.append("{}, {}".format(users_amount, tasks_amount))

    try:

        # Write the data to the user_overview.txt file  . The first line in the file contains the amount of users and tasks
        # The rest of the file will contain all data, each line a different user
        f = open('user_overview.txt', 'w+')
        f.write("{}\n".format(user_overview_list_general[0]))
        for x in range(0, len(user_overview_list)):
            f.write("{}".format(user_overview_list[x]))
        f.close()

    except FileNotFoundError:
        print("An error has occured with opening the data file. Check user_overview function.")

#===== Login Section =====

print("Welcome to the Task Manager App")

# Declare variables for use in this section but also for the rest of the program
username = ""
password = 0
all_users = []
all_passwords = []
username_valid = False
password_valid = False

# Open the user.txt file and split the usernames into list all_users and passwords into list all_passwords
f = open('user.txt', 'r')
for line in f:
    split_line = line.split(", ")
    all_users.append(split_line[0])
    all_passwords.append(split_line[1].strip("\n"))  
f.close()

# Create a dictionary with all the usernames and passwords saved for easy access instead of two list
all_users_dict = {}
for x in range(0, len(all_users)):
    all_users_dict[all_users[x]] = all_passwords[x]

# Get all tasks and place in a list called all_tasks
# Read all the lines of the tasks file and get the total amount of tasks in users.txt
total_num_of_tasks  = 0
all_tasks = []

f = open('tasks.txt', 'r')
for line in f:
    all_tasks.append(line)
    total_num_of_tasks +=1

# Check if the username is valid
# The While Loop checks if the username is anywhere in the all_users list and saves the index for password in pass_num
while username_valid == False:

    username = input("Username: ")
        
    if username in all_users:
        pass_num = all_users.index(username)
        username_valid == True
        break
    print("\nPlease make sure your spelling is correct or that the user does exist.\n")
            
# Check if the password is correct with the while loop
# The number that the username takes in all_users is the number used to check for the password in all_passwords
while password_valid == False:

    password = input("Password: ")

    if password == all_passwords[pass_num]:
        password_valid == True
        break   
    print("\nYour password is incorrect. Please try again.\n")
print("\nLogin Successful!\n")

# Use function to show the main menu once user is signed in.
main_menu(username, all_users, all_tasks, total_num_of_tasks)