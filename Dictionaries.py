# Holds inventory and price dictionary and all functions for orders, displaying and altering inventory
class CategoryDicts:
    def __init__(self, price_contents, inventory_contents):
        self.prices_dict = {}
        self.inventory_dict = {}
        self.total_earnings = 0
        self.UpdateDicts(price_contents, inventory_contents)

    # Displays inventory by category or all categories. Shows all items in category and category worth. If all categories are selected, it also shows total inventory worth
    def DisplayInventory(self, category):
        # If user wants to display full inventory
        if category == "all":
            total_worth = 0
            # Prints out the category and contents for each category in inventory
            for item in self.inventory_dict:
                category_worth = 0
                print(f"{item}:", self.inventory_dict[item])
                # Gets price for each item in inventory and gets the category worth and adds it to the total inventory worth, then displays each category worth and total worth
                for type in self.inventory_dict[item]:
                    for weight in self.inventory_dict[item][type]:
                        price = self.prices_dict[item][type]
                        category_worth += float(weight) * float(price)
                print("Category worth:", f"${round(category_worth, 2)}", "\n")
                total_worth += category_worth
            print("Total inventory worth:", f"${round(total_worth, 2)}", "\n")
        # If user selects specific category, it prints out that category and it's contents, then gets the category worth and displays it
        elif category in self.inventory_dict:
            print(f"{category}:", self.inventory_dict[category])
            category_worth = 0
            for type in self.inventory_dict[category]:
                for weight in self.inventory_dict[category][type]:
                    price = self.prices_dict[category][type]
                    category_worth += float(weight) * float(price)
            print("Category worth:", f"${round(category_worth, 2)}", "\n")
        else:
            print("That is not a valid category")

    # Writes to inventory file every time an order is completed to update the inventory.
    def UpdateInventory(self, item):
        item_category = item[0]
        item_type = item[1]
        # If the type is burger or eggs, they are formatted to hold the quantity in the inventory file, not the weight. Must check that the quantity is larger or equal to the purchased amount
        # and then adjust the inventory amount accordingly. If the quantity is equal to the amount left, it deletes it from the inventory file entirely.
        if item_type == "burger" or item_type == "eggs":
            item_quantity = item[2]
            if int(self.inventory_dict[item_category][item_type][0]) >= int(item_quantity):
                old_val = int(self.inventory_dict[item_category][item_type][0])
                new_val = old_val - int(item_quantity)
                if new_val > 0:
                    self.inventory_dict[item_category][item_type][0] = new_val
                else:
                    del self.inventory_dict[item_category][item_type]
                inventory_file = open("Inventory_file", "w")
                for category in self.inventory_dict:
                    for type in self.inventory_dict[category]:
                        for weight in self.inventory_dict[category][type]:
                            line = f"{category} {type} {weight}\n"
                            inventory_file.write(line)
            else:
                print("You don't have enough inventory to sell that much")
        # If the type isn't burger or eggs, the file is formatted to hold the individual item weight. That specific item is then found in the inventory and removed. If the type would then
        # be empty, the type is removed entirely. If the category would then be empty, the categeory is removed entirely as well.
        else:
            item_weight = item[2]
            if len(self.inventory_dict[item_category][item_type]) > 1:
                self.inventory_dict[item_category][item_type].remove(item_weight)
            else:
                if len(self.inventory_dict[item_category]) > 1:
                    del self.inventory_dict[item_category][item_type]
                else:
                    del self.inventory_dict[item_category]
        # The inventory file is then rewritten
        inventory_file = open("Inventory_file", "w")
        for category in self.inventory_dict:
            for type in self.inventory_dict[category]:
                for weight in self.inventory_dict[category][type]:
                    line = f"{category} {type} {weight}\n"
                    inventory_file.write(line)
        inventory_file.close()
        self.inventory_dict = {}
        self.prices_dict = {}
        # The dictionaries are remade using the current files
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
        self.UpdateDicts(prices_contents, inventory_contents)
        inventory_file.close()
        prices_file.close()

    # Allows user to create an order. User selects items from inventory and when finished, the order total is displayed and the selected items are removed from the inventory
    def CreateOrder(self):
        exit_loop = False
        order_total = 0
        # Prompts user to select a category after displaying the index and name of each category. The user is then prompted to choose a type in that category after displaying the index and name
        # of each type in that category. If the type is burger or eggs, the user is then prompted to enter a quantity and the inventory is updated accordingly. If the type is not burger or
        # eggs, the user is prompted to select a weight, after each weight of that type are displayed. The inventory is then updated accordingly. The price for that individual item is then
        # calculated using the weight and the price in the prices dictionary or the quantity and the price. That item total is then added to the order total. This continues until the user
        # chooses to end the order. The order total is then displayed.
        while exit_loop is False:
            print("Please select a category")
            category_count = 0
            category_list = []
            for category in self.inventory_dict:
                print(f"[{category_count}]", category)
                category_count += 1
                category_list.append(category)
            user_category = input()
            user_category = category_list[int(user_category)]
            if user_category in self.inventory_dict:
                type_count = 0
                type_list = []
                print("Please select a type: ")
                for type in self.inventory_dict[user_category]:
                    print(f"[{type_count}]", type)
                    type_count += 1
                    type_list.append(type)
                user_type = input()
                user_type = type_list[int(user_type)]
                if user_type in self.inventory_dict[user_category]:
                    if user_type == "burger" or user_type == "eggs":
                        print("Please enter quantity")
                        user_quantity = input()
                        if int(user_quantity) <= int(self.inventory_dict[user_category][user_type][0]):
                            price = self.prices_dict[user_category][user_type]
                            order_total += float(user_quantity) * float(price)
                            self.UpdateInventory([user_category, user_type, user_quantity])
                            print("Press 0 to add another item or 1 to continue to checkout")
                            user_exit = input()
                            if user_exit == "1":
                                exit_loop = True
                        else:
                            print("That is not a valid quantity")
                    else:
                        weight_count = 0
                        weight_list = []
                        print("Please select a weight")
                        for weight in self.inventory_dict[user_category][user_type]:
                            print(f"[{weight_count}]", weight)
                            weight_count += 1
                            weight_list.append(weight)
                        user_weight = input()
                        user_weight = weight_list[int(user_weight)]
                        if user_weight in self.inventory_dict[user_category][user_type]:
                            price = self.prices_dict[user_category][user_type]
                            order_total += float(user_weight) * float(price)
                            self.UpdateInventory([user_category, user_type, user_weight])
                            print("Press 0 to add another item or 1 to continue to checkout")
                            user_exit = input()
                            if user_exit == "1":
                                exit_loop = True
                        else:
                            print("That is not a valid weight")
                else:
                    print("That is not a valid type")
            else:
                print("That is not a valid category")
        print("Your order total is", f"${round(order_total, 2)}")
        self.total_earnings += order_total

    # Exactly the same as CreateOrder, except the inventory is not updated.
    def PriceCheck(self):
        exit_loop = False
        order_total = 0
        while exit_loop is False:
            print("Please select a category")
            category_count = 0
            category_list = []
            for category in self.inventory_dict:
                print(f"[{category_count}]", category)
                category_count += 1
                category_list.append(category)
            user_category = input()
            user_category = category_list[int(user_category)]
            if user_category in self.inventory_dict:
                type_count = 0
                type_list = []
                print("Please select a type: ")
                for type in self.inventory_dict[user_category]:
                    print(f"[{type_count}]", type)
                    type_count += 1
                    type_list.append(type)
                user_type = input()
                user_type = type_list[int(user_type)]
                if user_type in self.inventory_dict[user_category]:
                    if user_type == "burger" or user_type == "eggs":
                        print("Please enter quantity")
                        user_quantity = input()
                        if int(user_quantity) <= int(self.inventory_dict[user_category][user_type][0]):
                            price = self.prices_dict[user_category][user_type]
                            order_total += float(user_quantity) * float(price)
                            print("Press 0 to add another item or 1 to continue to checkout")
                            user_exit = input()
                            if user_exit == "1":
                                exit_loop = True
                        else:
                            print("That is not a valid quantity")
                    else:
                        weight_count = 0
                        weight_list = []
                        print("Please select a weight")
                        for weight in self.inventory_dict[user_category][user_type]:
                            print(f"[{weight_count}]", weight)
                            weight_count += 1
                            weight_list.append(weight)
                        user_weight = input()
                        user_weight = weight_list[int(user_weight)]
                        if user_weight in self.inventory_dict[user_category][user_type]:
                            price = self.prices_dict[user_category][user_type]
                            order_total += float(user_weight) * float(price)
                            print("Press 0 to add another item or 1 to continue to checkout")
                            user_exit = input()
                            if user_exit == "1":
                                exit_loop = True
                        else:
                            print("That is not a valid weight")
                else:
                    print("That is not a valid type")
            else:
                print("That is not a valid category")
        print("Your order total is", f"${round(order_total, 2)}")

    # When the main program is exited, the total earnings for that session are displayed
    def TotalEarnings(self):
        print("Your total earnings for this session are", f"${round(self.total_earnings, 2)}")

    # Takes in file contents to update the prices and inventory dictionaries. Called in UpdateInventory
    def UpdateDicts(self, price_contents, inventory_contents):
        for line in price_contents:
            category = line[0]
            type = line[1]
            price = line[2]
            if category in self.prices_dict:
                if type not in self.prices_dict[category]:
                    self.prices_dict[category][type] = price
            elif category not in self.prices_dict:
                self.prices_dict[category] = {}
                self.prices_dict[category][type] = price

        for line in inventory_contents:
            category = line[0]
            type = line[1]
            weight = line[2]
            if category in self.inventory_dict:
                if type not in self.inventory_dict[category]:
                    self.inventory_dict[category][type] = [weight]
                elif type in self.inventory_dict[category]:
                    self.inventory_dict[category][type].append(weight)
            elif category not in self.inventory_dict:
                self.inventory_dict[category] = {}
                self.inventory_dict[category][type] = [weight]
        for category in self.inventory_dict:
            for type in self.inventory_dict[category]:
                self.inventory_dict[category][type].sort()
