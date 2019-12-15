from Dictionaries import *

# File for main program to run in. Loops until user enters exit command
def main():
    # Opens and reads from inventory and prices file, then creates the dictionary object with these contents.
    inventory_file = open("Inventory_file", "r")
    inventory_lines = inventory_file.readlines()
    inventory_contents = []
    for line in inventory_lines:
        inventory_contents.append(line.split())
    prices_file = open("Prices_file", "r")
    prices_lines = prices_file.readlines()
    prices_contents = []
    for line in prices_lines:
        prices_contents.append(line.split())
    inventory_file.close()
    prices_file.close()
    dictionaries = CategoryDicts(prices_contents, inventory_contents)
    exit_main = False
    command_list = ["Display inventory", "Start an order", "Price check an order", "Exit program"]
    print("Welcome to Farmer's Helper!")
    # Loops and prompts user to select from the given commands. Display inventory calls the DisplayInventory function, Start an order calls the CreateOrder function, Price check an order calls
    # the PriceCheck function and Exit program ends the loop, thus displaying the session total between all orders and ends the program.
    while exit_main is False:
        print("Select one of the options below")
        command_count = 0
        for command in command_list:
            print(f"[{command_count}]", command)
            command_count += 1
        user_command = input()
        user_command = command_list[int(user_command)]
        category_count = 0
        category_list = []
        if user_command == "Display inventory":
            print("Select a category to display")
            for category in dictionaries.inventory_dict:
                print(f"[{category_count}]", category)
                category_list.append(category)
                category_count += 1
            print(f"[{category_count}]", "all")
            all_count = category_count
            user_category = input()
            if int(user_category) == all_count:
                dictionaries.DisplayInventory("all")
            else:
                user_category = category_list[int(user_category)]
                dictionaries.DisplayInventory(user_category)
        elif user_command == "Start an order":
            dictionaries.CreateOrder()
        elif user_command == "Price check an order":
            dictionaries.PriceCheck()
        elif user_command == "Exit program":
            exit_main = True
    dictionaries.TotalEarnings()
    return 0

main()