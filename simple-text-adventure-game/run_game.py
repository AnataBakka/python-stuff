import math, sys, importlib, random
import exceptions

def check_input(*args,back = False, forward = False, quitting = True, invis_choices = None,\
                vis_choices = None):
    """Checks user input until it's equal to one of the values in the given \
parameters.
        Args:
                args: non key-ed parameters are put in a list which the user \
                would need to input their index.

                back (boolean): returns "back" if selected

                forward (boolean): returns "forward" if selected

                quitting (boolean): raises UserExit if selected

                invis_choices (list): list of values that are not visible to \
                the user but allows them to exit the loop by inputting them

                vis_choices (dictionary): dictionary of values that are \
                visible to the user and allows them to exit the loop by inputting \
                their key
        Returns:
                value: value selected
        Raises:
                UserExit: upon selecting 'quitting'
    """
    while True:
        string = []

        if args:
            temp_string = []
            args_size = len(args)

            for i in range(args_size):
                temp_string.append(str(i)+"."+str(args[i]))

            string.append("\n".join(temp_string))

        if vis_choices:
            temp_string = []

            for i,v in vis_choices.items():
                temp_string.append(str(i)+"."+str(v))

            string.append("\n".join(temp_string))

        if back or forward or quitting:
            temp_string = []

            if back:
                temp_string.append("Z.Back ")

            if forward:
                temp_string.append("Y.Forward ")

            if quitting:
                temp_string.append("X.Quit")

            string.append("".join(temp_string))

        if string:
            print("\n\n".join(string))

        input_choice = input("> ")
        print()

        try:
            input_choice = int(input_choice)
        except ValueError:
            input_choice = input_choice.upper()
        else:
            if args and input_choice < args_size:
                if input_choice >= 0:
                    return input_choice

            input_choice = str(input_choice)

        if input_choice in ("Z","Y","X"):
            if input_choice == "X" and quitting:
                print("Are you sure you want to exit? (y/n)")

                while True:
                    input_choice = input("> ").lower()
                    print()

                    if input_choice == "y":
                        raise exceptions.UserExit

                    if input_choice == "n":
                        break

                    print("Invalid input!")

                continue

            if input_choice == "Z" and back:
                return "back"

            if input_choice == "Y" and forward:
                return "forward"

        if invis_choices is not None:
            for i in invis_choices:
                if str(i).upper() == input_choice:
                    return i

        if vis_choices is not None:
            for i in vis_choices:
                if str(i).upper() == input_choice:
                    return i

        print("Input not available!\n")
        continue

def welcome():
    """Prints a welcome message upon starting the program."""
    print("Welcome to Monster RPG!\n"+\
          "In this game you choose one adventurer, and well... you start the\n"+\
          "game and adventure. The adventure will only end when you die.")

def load_chars(type_of_chars = "main"):
    """Returns a list of characters based on 'type_of_chars'.
        Args:
                type_of_chars (string): if 'main' it returns main characters \
                else it returns enemy characters
        Returns:
                list: list of chosen type of characters
    """
    if type_of_chars == "main":
        file_name = "main_character_list.txt"
    else:
        file_name = "enemy_character_list.txt"

    character_list = []

    with open(file_name) as file:
        for character in file:
            character = character.strip()
            character_list.append(character)

    return character_list

def spawn_character(char_name):
    """Returns the 'char_name' character class.
        Args:
                char_name (string): character file_name
        Returns:
                class: character class
    """
    lib = importlib.import_module(char_name)
    return lib.Character

def choose_character():
    """Used for returning the class of a chosen main character.
        Returns:
                class: chosen character class
    """
    print("Choose your character!\n")
    character_list = load_chars("main")
    input_choices = {"character_class":[],"character_name":[]}

    for i in character_list:
        character_class = spawn_character(i)
        input_choices["character_class"].append(character_class)
        input_choices["character_name"].append(character_class().name)

    input_choice = check_input(*input_choices["character_name"])
    return input_choices["character_class"][input_choice]

class world_object():
    def __init__(self):
        self.__world = {}
        self.__main_paths = []
        self.__current_main_path = -1
        self.__default_events =  {"north":"south","south":"north","west":"east","east":"west"}
        self.__paths_converged = False
        self.area_count = 0

    def get_default_events(self):
        """Returns the dictionary of default events.
            Returns:
                    dictionary: default events
        """
        return self.__default_events

    def add_area(self,object_area,events = {}):
        """Adds 'object_area' to the world with the chosen 'events'.
            Args:
                    object_area (object): area to add to the world
                    events (dictionary): event:consequence
        """
        coord = object_area.coord
        self.__world[coord] = {"area":object_area,"move_events":events}
        self.area_count += 1

    def get_area(self,coord = None):
        """Returns the object area with 'coord' from the world, or else returns \
current area.
            Args:
                    coord (tuple): coords of the area to return
            Returns:
                    object: area object
        """
        if coord:
            return self.__world[coord]["area"]

        return self.__world[self.__current_area]["area"]

    def add_coord_to_path(self,coord):
        """Adds 'coord' to the current main path.
            Args:
                    coord (tuple): coord of an area to add
        """
        self.__main_paths[self.__current_main_path].append(coord)

    def create_new_path(self,coord):
        """Creates a new main path with the starting 'coord'.
            Args:
                    coord (tuple): coord to add to new main path
        """
        self.__main_paths.append([coord])
        self.__current_main_path = len(self.__main_paths)-1

    def get_current_path(self):
        """Returns a copy of the list of coords in the current main path.
            Returns:
                    list: list of tuples
        """
        return self.__main_paths[self.__current_main_path].copy()

    def get_path_indexes(self,*coords):
        """Returns a list of the indexes of the path where each 'coord' is found.
            Args:
                    coords: coords whose path needs checked
            Returns:
                    list: list of path indexes
        """
        check_coords = list(coords)

        for coord_index, coord in enumerate(check_coords):
            for path_index,path in enumerate(self.__main_paths):
                if coord in path:
                    check_coords[coord_index] = path_index
                    break

        return check_coords

    def combine_paths(self,path_table):
        """Combines main paths by using the indexes from 'path_table'.
            Args:
                    path_table (list): list of indexes
        """
        new_path = []
        path_table.sort(reverse = True)
        #The reverse is to make sure the table doesn't messes up during the cycle.
        #(upon removing an index higher than the others from the table)

        for path in path_table:
            new_path += self.__main_paths[path]
            del self.__main_paths[path]

        self.__main_paths.append(new_path)
        self.__paths_converged = True
        self.__current_main_path = len(self.__main_paths)-1

    def are_paths_converged(self):
        """Returns True or False based on whether paths have been converged or not.
            Returns:
                    boolean: based on paths having been converged
        """
        if self.__paths_converged:
            self.__paths_converged = False

            return True

        return False

    def change_current_area(self,coord):
        """Changes current area pointer.
            Args:
                    coord (tuple): tuple area coords pointer
        """
        self.__current_area = coord

    def get_event_consequence(self,event):
        """Returns the consequence of an event of the current area.
            Args:
                    event (string): event whose consequence wants to be returned
            Returns:
                    variable: consequence of the event
        """
        self.__current_area = self.__world[self.__current_area]["move_events"][event]
        return self.__current_area

    def get_events(self):
        """Returns a list of all possible events of the current area.
            Returns:
                    list: events of current area
        """
        return list(self.__world[self.__current_area]["move_events"].keys())

    def add_nearby_events(self,current_coord):
        """Used upon creating a new area. Adds each opposite event of current \
area to all nearby areas, while also adding the opposite events of nearby areas \
to current area.
            Args:
                    current_coord (tuple): coord of area to add nearby events
        """
        current_x = current_coord[0]
        current_y = current_coord[1]

        for event in self.__default_events:
            x = current_x
            y = current_y

            if event == "north":
                y += 1
            elif event == "south":
                y -= 1
            elif event == "west":
                x -= 1
            elif event == "east":
                x += 1

            nearby_area_coords = (x,y)

            if self.__world.get(nearby_area_coords) is not None:
                temp_event = self.__default_events[event]

                if self.__world[nearby_area_coords]["move_events"].get(temp_event) is not None:
                    self.__world[current_coord]["move_events"][event] = nearby_area_coords
                else:
                    self.__world[current_coord]["move_events"].pop(event,None)

    def get_new_coords(self,old_coords,events = None, delta = 1):
        """Returns a dictionary of each 'event' with its corresponding area \
coordinate.
            Args:
                    old_coords (tuple): coord to add the events to
                    events (list): events to add to the coord
                    delta (number): how far away is the new area
            Returns:
                    dictionary: event:coord
        """
        old_x = old_coords[0]
        old_y = old_coords[1]
        result = {}

        for event in events:
            x = old_x
            y = old_y

            if event == "north":
                y += delta
            elif event == "south":
                y -= delta
            elif event == "west":
                x -= delta
            elif event == "east":
                x += delta

            result[event] = (x,y)

        return result

    def set_starting_coord(self,coord):
        """Sets starting coord. Used for get_level().
            Args:
                    coord (tuple): coord to set
        """
        self.__starting_coord = coord

    def get_level(self):
        """Returns the level of the current_area based on the distance from \
starting coord.
            Returns:
                    number: level of current_area
        """
        return int(math.sqrt((self.__current_area[0]-self.__starting_coord[0])\
                             **2+(self.__current_area[1]-self.__starting_coord[1])**2))

    def has_shop_been_found(self,boolean = "get"):
        """Used for adding a boolean value to an attribute to then check it \
with the value 'get' of the same 'boolean' parameter.
            Args:
                    boolean (string / boolean): 'get' / boolean
            Returns:
                    boolean: only if 'boolean' is 'get'
        """
        if boolean == "get":
            return self.__has_shop_been_found

        self.__has_shop_been_found = boolean
        return None

    def safe_event(self,event = "get"):
        """Used for adding an 'event' to an attribute to then check it \
with the value 'get' of the same 'event' parameter.
            Args:
                    event (string): 'get' / string
            Returns:
                    string: only if 'event' is 'get'
        """
        if event == "get":
            return self.__safe_event

        self.__safe_event = event
        return None

    def has_beaten_final_boss(self,boolean = "get"):
        """Used for adding a boolean value to an attribute to then check it \
with the value 'get' of the same 'boolean' parameter.
            Args:
                    boolean (string / boolean): 'get' / boolean
            Returns:
                    boolean: only if 'boolean' is 'get'
        """
        if boolean == "get":
            return self.__final_boss_beaten

        self.__final_boss_beaten = boolean
        return None

class area_object():
    def __init__(self,coord):
        self.__objects = []
        self.__enemies = []
        self.__allies = []
        self.coord     = coord
        self.__objects_inspected = False

    def remove_object(self,object_item):
        """Removes 'object_item' from the list of objects in the area.
            Args:
                    object_item (object): object to remove
        """
        self.__objects.remove(object_item)

    def get_objects(self):
        """Returns a copy of the list of objects in the area.
            Returns:
                    list: objects
        """
        return self.__objects.copy()

    def add_object(self,object_item):
        """Adds 'object_item' to the list of objects in the area.
            Args:
                    object_item (object): object to add to the area
        """
        self.__objects.append(object_item)

    def add_enemy(self,object_enemy):
        """Adds 'object_enemy' to the list of enemies in the area.
            Args:
                    object_enemy (object): object to add to the area
        """
        self.__enemies.append(object_enemy)

    def add_ally(self,object_ally):
        """Adds 'object_ally' to the list of allies in the area.
            Args:
                    object_ally (object): object to add to the area
        """
        self.__allies.append(object_ally)

    def get_enemies(self):
        """Returns the list of enemies from the area.
            Returns:
                    list: list of enemy objects
        """
        return self.__enemies

    def get_allies(self):
        """Returns the list of allies from the area.
            Returns:
                    list: list of ally objects
        """
        return self.__allies

    def have_inspected_objects(self,boolean = "get"):
        """Used for adding a boolean value to an attribute to then check it \
with the value 'get' of the same 'boolean' parameter.
            Args:
                    boolean (string / boolean): 'get' / boolean
            Returns:
                    boolean: only if 'boolean' is 'get'
        """
        if boolean == "get":
            return self.__objects_inspected

        self.__objects_inspected = boolean
        return None

class inventory_object():
    def __init__(self,main_char):
        self.__items = {}
        self.__main_char = main_char
        self.__gold = 0

    def add_gold(self,amount):
        """Adds an 'amount' of gold to the inventory.
            Args:
                    amount (number): amount of gold
        """
        self.__gold += amount

    def remove_gold(self,amount):
        """Removes an 'amount' of gold from the inventory.
            Args:
                    amount (number): amount of gold
        """
        self.__gold -= amount

        if self.__gold < 0:
            self.__gold = 0

    def get_gold(self):
        """Returns the amount of gold in the inventory.
            Returns:
                    number: amount of gold
        """
        return self.__gold

    def get_items(self):
        """Returns a dictionary of the items in the inventory.
            Returns:
                    dictionary: name:"object"/"amount"
        """
        return self.__items

    def add_item(self,item_object,amount = 1):
        """Adds the 'item_object' an 'amount' of times to the inventory.
            Args:
                    item_object (object): item object to add
                    amount (number): amount of times to add it
            Returns:
                    boolean: True or None based on the object being successfully \
                    added to the inventory or not
        """
        name = item_object.name.upper()

        try:
            item_object.consumable
        except AttributeError:
            if name in self.__items:
                print("Note that adding this item to the inventory will overwrite the "+\
                      "existing one. Confirm?")
                print("Current: {}".format(self.__items[name]["object"].description))
                print("New one: {}\n".format(item_object.description))

                input_choice = check_input(vis_choices = {"Y":"Yes","N":"No"})

                if input_choice == "N":
                    return None

                self.remove_item(self.__items[name]["object"])

        if name in self.__items:
            self.__items[name]["amount"] += amount
        else:
            self.__items[name] = {}
            self.__items[name]["object"] = item_object
            self.__items[name]["amount"] = amount

            try:
                item_object.passive
            except AttributeError:
                pass
            else:
                self.__main_char.grant_permanent_buff(item_object)

        return True

    def remove_item(self,item_object,amount = 1):
        """Remove the 'item_object' an 'amount' of times to the inventory.
            Args:
                    item_object (object): item object to remove
                    amount (number): amount of times to remove it
        """
        name = item_object.name.upper()
        self.__items[name]["amount"] -= amount

        if self.__items[name]["amount"] <= 0:
            self.__items.pop(name)

            try:
                item_object.passive
            except AttributeError:
                pass
            else:
                self.__main_char.remove_permanent_buff(item_object)

    def show_inventory(self, consumables_only = False):
        """Prints the current items in the inventory in a formatted way, while \
also asking the user if they want to consume any available items.
            Args:
                    consumables_only (boolean): used for showcasing consumables \
                    only or not
        """
        while True:
            s = []
            item_list = []
            count = 0
            found_consumable = False

            for v in self.__items.values():
                try:
                    v["object"].consumable
                except AttributeError:
                    if consumables_only:
                        continue
                else:
                    if not found_consumable:
                        found_consumable = True

                item_list.append(v)
                s.append((str(count) + ". ").ljust(20) + v["object"].name.\
                         ljust(20) + str(v["amount"]) + "\n"+v["object"].description)
                count += 1

            print("Owned gold: {}".format(self.__gold))

            if s:
                print("Item index".ljust(20) + "Item name".ljust(20) + "Amount")
                print("\n\n".join(s))

                if not found_consumable:
                    break

                print("\nTo consume an item input their index.\n")
                input_choice = check_input(invis_choices = range(len(item_list)),back = True)

                if input_choice == "back":
                    break

                input_item = item_list[input_choice]

                try:
                    input_item["object"].consumable
                except AttributeError:
                    print("You cannot consume that item!\n")
                    continue

                while True:
                    input_amount = input("Choose the amount:\n> ")
                    print()

                    try:
                        input_amount = int(input_amount)
                    except ValueError:
                        pass
                    else:
                        if 0 < input_amount <= input_item["amount"]:
                            self.activate(input_item["object"].name, input_amount)

                        break

                    print("Invalid number! Put 0 if you want to back.")

                continue

            if consumables_only:
                print("You don't have any consumables in the inventory!")
            else:
                print("You don't have any items in the inventory!")

            break

    def activate(self,item_name,amount = 1):
        """Activate the item_name from the inventory an 'amount' of times \
if possible.
            Args:
                    item_name (string): item name
                    amount (value): amount of times to activate
        """
        item_name = item_name.upper()

        for i in range(amount):
            try:
                self.__items[item_name]["object"].active(self.__main_char)
            except exceptions.ItemError as err_msg:
                print(err_msg)
                print("The item has only been activated {} times.".format(i))
                self.remove_item(self.__items[item_name]["object"],i)
                return

        self.remove_item(self.__items[item_name]["object"],amount)
        print("You have used the item!")

class shop():
    def __init__(self,main_char = None,current_level = 0):
        self.name = "Shop"
        self.__level = current_level

        if main_char:
            self.__inventory = main_char.get_inventory()

    def get_shop(self):
        """Prints the items in the shop while also asking for user input if they \
want to buy something."""
        import item_list

        while True:
            print("Owned gold: {}".format(self.__inventory.get_gold()))
            input_choices = {"item_object":[],"item_name":[]}

            for item_object in item_list.item_object_list:
                input_choices["item_object"].append(item_object)
                input_choices["item_name"].append(item_object().name)

            input_choice = check_input(*input_choices["item_name"],back = True)

            if input_choice == "back":
                return

            try:
                input_item = input_choices["item_object"][input_choice](self.__level)
            except TypeError:
                input_item = input_choices["item_object"][input_choice]()

            print(input_item.description+"\n"+"Cost:",input_item.cost)

            if self.__inventory.get_gold() < input_item.cost:
                print("You don't have enough gold to buy this item!\n")
                continue

            print("Do you want to buy it?\n")
            input_choice = check_input(vis_choices = {"Y":"Yes","N":"No"})

            if input_choice == "N":
                continue

            try:
                input_item.consumable
            except AttributeError:
                check_for_success = self.__inventory.add_item(input_item)

                if check_for_success:
                    self.__inventory.remove_gold(input_item.cost)
                    print("Item successfully bought!")
            else:
                if input_item.consumable:
                    print("Input the amount you want to buy:")

                    while True:
                        input_choice = input("> ")
                        print()

                        try:
                            input_choice = int(input_choice)
                        except ValueError:
                            print("You need to input an integer number!")
                        else:
                            if input_choice == 0:
                                break

                            if input_choice < 0:
                                print("You cannot input negative numbers!")
                                continue

                            if self.__inventory.get_gold() < input_item.cost*input_choice:
                                print(("You don't have enough gold!\n"+\
                                      "The maximum amount you can buy is {}.")\
                                      .format(input_item.cost*input_choice//self.__inventory.get_gold()))
                                continue

                            check_for_success = self.__inventory.add_item(input_item, amount = input_choice)

                            if check_for_success:
                                self.__inventory.remove_gold(input_item.cost*input_choice)
                                print("Item successfully bought!")

                            break

class gold():
    def __init__(self,amount = 0):
        self.name = "Gold"
        self.amount = amount

def combat(allied_units, enemy_units, final_boss = False):
    """Combat system. 'allied_units' against 'enemy_units'.
        Args:
                allied_units (list): list of allied objects
                enemy_units (list): list of enemy objects
                final_boss (boolean): whether the combat is for the final \
                boss or not
        Returns:
                string: 'User_lost' / 'User_won' / 'User_left_combat'
    """

    main_char = allied_units[0]
    main_char_abilities = (*main_char.get_abilities().values(),)
    all_units = [allied_units,enemy_units]

    while True:
        for team_index, team in enumerate(all_units):
            if team_index == 1:
                print("Enemies:\n")

            for char in team:
                char.get_update()

        for team_index,team in enumerate(all_units): # Cycles through the teams
            enemies = all_units[abs(team_index-1)] #Enemies are always the opposite team

            for char_index, char in enumerate(team): # Cycles through each char in team
                if char.cannot_act:
                    continue

                if char == main_char and not main_char.is_controlled:
                    while True:
                        input_choices = {"A":"Normal Attack", "Q":main_char_abilities[0],\
                                         "W":main_char_abilities[1],"E":main_char_abilities[2],"H": "Help",\
                                         "I":"Inventory", "L": "Leave Combat"}

                        if final_boss:
                            input_choices.pop("I")
                            input_choices.pop("L")

                        if main_char.is_dev():
                            input_choices["K"] = "Kill Everyone"

                        input_choice = check_input(vis_choices = input_choices)

                        if input_choice == "H":
                            combat_help(main_char)
                            print()
                            continue

                        if input_choice == "I":
                            main_char.get_inventory().show_inventory(consumables_only = True)
                            print()
                            continue

                        if input_choice == "L":
                            return "User_left_combat"

                        if input_choice == "K":
                            break

                        try:
                            ability = main_char.use_ability(input_choice, all_units = all_units)
                        except exceptions.AbilityError as err_msg:
                            print(err_msg)
                            print()
                            continue

                        main_char.current_mana -= ability.mana
                        break
                else:
                    ability = char.random_ability(all_units = all_units)

                gold_received = 0

                if input_choice == "K":
                    i = len(enemies)-1

                    while i >= 0:
                        gold_received += enemies[i].gold
                        del enemies[i]
                        i -= 1
                elif ability.affects == "self":
                    ability.trigger(char)
                elif ability.affects == "aoe_enemy":
                    i = len(enemies)-1

                    while i >= 0:
                        enemy_chosen = enemies[i]
                        ability.trigger(enemy_chosen)

                        if enemy_chosen.check_hp_status() == "CharacterDead":
                            if enemy_chosen == main_char:
                                return "User_lost"

                            gold_received += enemy_chosen.gold
                            del enemies[i]

                        i -= 1
                elif ability.affects == "enemy":
                    if len(enemies) == 1:
                        enemy_index = 0
                    elif char != main_char:
                        enemy_index = random.randrange(len(enemies))
                    else:
                        input_choices = ()

                        for i in enemies:
                            input_choices += (i.name,)

                        print("Choose your target.\n")
                        enemy_index = check_input(*input_choices, back = True)

                        if enemy_index == "back":
                            continue

                    enemy_chosen = enemies[enemy_index]
                    ability.trigger(enemy_chosen)

                    if enemy_chosen.check_hp_status() == "CharacterDead":
                        if enemy_chosen == main_char:
                            return "User_lost"

                        gold_received += enemy_chosen.gold
                        del enemies[enemy_index]

                if gold_received and team_index == 0:
                    main_char.get_inventory().add_gold(gold_received)
                    print("You have looted {} Gold!".format(gold_received))

                if not enemy_units: # Adding the check for controlled units
                    stop = False
                    temp_team_index = team_index
                    temp_team = team

                    for team_index, team in enumerate(all_units):
                        for char_index, char in enumerate(team):
                            if char.is_controlled:
                                del team[char_index]
                                all_units[abs(team_index-1)].append(char)
                                char.is_controlled = False
                                stop = True
                                break

                        if stop:
                            break

                    if not stop:
                        print("You won!")
                        return "User_won"

                    team_index = temp_team_index
                    team = temp_team

        for team in all_units:
            for char in team:
                char.round_events()

def combat_help(self):
    """Prints the description of abilities if they're castable, plus any active buffs \
on the character."""
    import buff_list

    ability_list_names = self.get_abilities()

    for i in ["A","Q","W","E"]:
        print()
        print(ability_list_names.get(i) or "Normal attack")

        try:
            ability = self.use_ability(i)
        except exceptions.AbilityError as err_msg:
            print("Cannot see the details of the ability if it cannot be cast.")
            print(err_msg)
            continue

        mana = ability.mana

        try:
            description = ability.description
        except AttributeError:
            description = None

        try:
            dmg = ability.dmg
        except AttributeError:
            dmg = None

        affects = ability.affects
        buff_name = None
        rounds = None

        try:
            ability.buff_class
        except AttributeError:
            pass
        else:
            buff_name = ability.buff_class().name
            rounds = ability.rounds

        if description:
            print(description)
        else:
            if dmg:
                print("Deals damage to ",end="")

            if buff_name:
                print("Grants "+buff_name+" to ",end="")

            if affects == "enemy":
                print("a single enemy",end="")
            elif affects == "aoe_enemy":
                print("all enemies",end="")
            elif affects == "self":
                print("self",end="")

            if rounds:
                print(" for {} rounds".format(rounds),end="")

            print(".")

        print("Mana: {}".format(mana))

        if dmg:
            print("Damage: {}".format(dmg))

        if buff_name:
            print("Buff name: {}".format(buff_name))
            print(buff_list.get_description().get(buff_name))

    active_buffs = self.get_buffs()

    if active_buffs:
        print()
        print("Currently active buffs:")
        print("Name".ljust(20),"Remaining Rounds")

        for i,v in active_buffs.items():
            print(i.name.ljust(20),v)

def world_help(commands):
    """Prints out the possible commands with their respective descriptions.
        Args:
                commands (list): list of all available commands
    """
    print("Commands: 'move'","".join([", '"+i+"'" for i in commands]))
    print("\nMove: 'north', 'south', 'west', 'east'.")

    if "inventory" in commands:
        print("\nInventory: showcases the items you got. You may also consume any\n"+\
              "consumable items if available.")

    if "teleport" in commands:
        print("\nTeleport: Once you clear an area (of objects and enemies), the area\n"+\
              "will forever be empty. Since it's not fun going through empty areas\n"+\
              "when moving back, you should then simply teleport to the desired\n"+\
              "location!")
        if "main path" in commands:
            print("Note: You may only teleport to areas you have discovered that are linked\n"+\
                  "by a main path.")

    if "main path" in commands:
        print("\nMain path: showcases any available main paths. Main paths are guaranteed\n"+\
              "to reach a village. Going through the main path is ideal, as you cannot\n"+\
              "get lost. However, sometimes, the main path is blocked, or is non\n"+\
              "existent, which means you're only able to go through the jungle, which\n"+\
              "has no guarantee of allowing you to return back. Enemies are also more\n"+\
              "likely to get an unexpected increase of strenght.\n"+\
              "Note: Once you find a shop you will once again be able to see\n"+\
              "the coordinates you're in. Also, if you manage to return to a previous path\n"+\
              "you will link the current one with that one, allowing you to increase\n"+\
              "the amount of locations you can teleport to!")

    if "inspect" in commands:
        print("\nInspect: you can inspect areas to see if there's any shop or available\n"+\
              "item to take.")
        print("You can only access these objects on the map after using this command.")

    if "status" in commands:
        print("\nStatus: returns your character's status.")

    if "save" in commands:
        print("\nSave: saves the current state of this world to allow you to continue at\n"+\
              "the next runtime.")

    if "be a dev" in commands:
        print("\nBe a Dev: kind of a hack. You got super powers, unlocking new commands\n"+\
              "which let you change the world around you. You also have\n"+\
              "unlimited power and can instantly kill all enemies before you.")

    if "add" in commands:
        print("\nAdd: 'area', 'object'.")

    if "die" in commands:
        print("\nDie: End the game.")

def load(file_name,data_type = {}):
    """Loads the 'file_name' and returns its contents with the default of \
'data_type'.
        Args:
                file_name (string): file to load
                data_type (variable): what should return if the file is empty \
                or doesn't exist
        Returns:
                data: file data or 'data_type'
    """
    import pickle #adding the import here instead of global for efficiency

    try:
        file = open(file_name, 'rb')
    except FileNotFoundError:
        file = open(file_name, 'wb')
        file.close()
        return data_type
    except IOError:
        print(("The program encountered an error while trying to read the file "+\
              "\"{}\", and will now exit.").format(file_name),end="")
        input()
        sys.exit()

    if file.read():
        file.seek(0)
        data = pickle.load(file)
        file.close()
        return data

    file.close()
    return data_type

def save(data,file_name):
    """Saves 'data' to the 'file_name'.
        Args:
                data (variable): data to save
                file_name (string): file name in current directory to save the data
    """
    import pickle #adding the import here instead of global for efficiency

    with open(file_name, 'wb') as file:
        pickle.dump(data,file)

def save_game(saved_data):
    """Saves game saved_data to its respective loaded file.
        Args:
                saved_data (variable): data to save
    """
    print("Saving data...")
    file_name = saved_data.get("saved_file")
    save(saved_data,file_name)
    print("Save complete.")

def leaderboards(player_scores):
    """Prints out the 'player_scores' in a formatted way.
        Args:
                player_scores (dictionary): saved player scores
    """
    list_names = list(player_scores.keys())
    list_names.sort(reverse = True, key = player_scores.get)
    largest_score = math.log10(player_scores[list_names[0]])
    longest_name = len(max(player_scores,key = len))

    if largest_score < 9: # May be changed if wished.
        largest_score = 9

    largest_score += 1 # This is for the additional space between name and score

    if longest_name < 4: # 4 is the word's "Name" lenght
        longest_name = 4

    print("Score".ljust(largest_score)+"Name")
    print("-"*(largest_score + longest_name))

    for name in list_names:
        print(str(player_scores[name]).ljust(largest_score)+name)

def create_area(world,current_coord,events,unknown_area = True):
    """Adds an area with 'current_coord' and 'events' to the 'world' while also \
creating a new path or adding it to the current one based on 'unknown_area'.
        Args:
                world (object): world object to save the area to
                current_coord (tuple): coords to save the are with
                events (list): list of events to add to the created area
                unknown_area (boolean): switches between creating new path or \
                adding to existent
    """
    if unknown_area:
        world.create_new_path(current_coord)
    else:
        world.add_coord_to_path(current_coord)

    world.add_area(area_object(current_coord),world.get_new_coords(current_coord,events))
    world.add_nearby_events(current_coord)

def check_user_input_coords():
    """Checks whether the user correctly inputs the coords and then correctly \
returns it for the data.
        Returns:
                tuple: coords
    """
    while True:
        input_choice = input("> ")
        print()
        input_choice = input_choice.split(",")

        try:
            input_choice[2]
        except IndexError:
            try:
                input_choice[1]
            except IndexError:
                pass
            else:
                try:
                    return (int(input_choice[0]),int(input_choice[1]))
                except ValueError:
                    pass

        print("Invalid input! The coordinates need to be in the\n"+\
              "format of 'x,y', and must be numbers. Do you want to back instead?\n")

        input_choice = check_input(vis_choices = {"Y":"Yes","N":"No"})

        if input_choice == "Y":
            break

        print("Input the coordinates!")

    return None

class final_boss_object():
    def __init__(self):
        self.name = "Final Boss"

def main_game(saved_data):
    """Main game system.
        Args:
                saved_data (dictionary): dictionary which contains data needed \
                for the game to run correctly.
        Returns:
                string: 'User Lost'
    """
    if saved_data["objects"]:
        objects = saved_data["objects"]
        main_char = objects["main_char"]
        world = objects["world"]
        current_area = world.get_area()
        print("You're back in the game!")
    else:
        # Setting up the starting world
        main_char = choose_character()()
        main_char.add_inventory(inventory_object(main_char))
        world = world_object()
        current_coord = (random.randrange(1001),random.randrange(1001))
        current_area = area_object(current_coord)
        world.set_starting_coord(current_area.coord)

        if saved_data["difficulty"] == "Hard":
            events = []
        else:
            events = world.get_default_events()

        world.add_area(current_area,world.get_new_coords(current_coord,events))
        world.change_current_area(current_area.coord)
        world.create_new_path(current_area.coord)
        current_area.add_object(shop(main_char,world.get_level()))
        world.has_beaten_final_boss(False)

        if saved_data["difficulty"] == "Hard":
            world.has_shop_been_found(False)
        else:
            world.has_shop_been_found(True)

        world.safe_event(None)
        main_char.is_dev(False)
        saved_data["objects"] = {"main_char":main_char,"world":world}
        print("The adventure has started!")
        print("Input 'help' for more help.")

    if main_char.is_dev():
        main_char.is_dev(False)
        print("'Be a dev' has been disabled while you were gone. You need to reapply\n"+\
              "again if you wish so.")

    commands = ["inventory","teleport","main path","inspect","status","help","save","be a dev"]

    if saved_data["difficulty"] != "Normal":
        commands.remove("main path")

    if saved_data["difficulty"] == "Hard":
        commands.remove("teleport")

    all_possible_inputs = commands + ["move " + i for i in world.get_default_events()]

    while True:
        num_choices = []

        if current_area.have_inspected_objects() or main_char.is_dev():
            num_choices = [i.name for i in current_area.get_objects()]

            if "Shop" in num_choices and saved_data["difficulty"] != "Hard":
                world.has_shop_been_found(True)

        if len(num_choices) > 2:
            num_choices.append("Grab all items.")

        print("Area coordinates:",end=" ")

        if world.has_shop_been_found() or main_char.is_dev():
            print(current_area.coord)

            if world.are_paths_converged():
                print("You've converged some main paths! You can now teleport to more\n"+\
                      "locations!")
        else:
            print("???")

        if main_char.is_dev():
            for i in world.get_events():
                print(i)

        print()
        input_choice = check_input(*num_choices, invis_choices = all_possible_inputs)

        if input_choice == "inventory":
            main_char.get_inventory().show_inventory()
            print()
            continue

        if input_choice == "teleport":
            if main_char.is_dev():
                print("Input the coordinates you want to teleport to:")
                current_coord = check_user_input_coords()

                if not current_coord:
                    continue

                world.change_current_area(current_coord)

                try:
                    current_area = world.get_area()
                except KeyError:
                    create_area(world,current_coord,[],True)
                    print("The area has been created!")
                    current_area = world.get_area()
            elif world.has_shop_been_found():
                path_table = world.get_current_path()
                input_choices = ()

                for coord in path_table:
                    s = str(coord)
                    temp_area = world.get_area(coord)
                    objects = temp_area.get_objects()

                    if objects:
                        for item_object in objects:
                            if item_object.name == "Shop":
                                s += " There's a shop in this area!"
                                break

                    if temp_area.get_enemies():
                        s += " There're enemies in this area!"

                    input_choices += (s,)

                input_choice = check_input(*input_choices,back = True)

                if input_choice == "back":
                    continue

                current_coord = path_table[input_choice]
                world.change_current_area(current_coord)
                current_area = world.get_area()
            else:
                print("You cannot teleport from an unknown area!")

            continue

        if input_choice == "main path":
            main_path = world.get_events()

            if main_path:
                for i in main_path:
                    print(i)
            else:
                print("There's no main path!")

            print()
            continue

        if input_choice == "inspect":
            current_objects = current_area.get_objects()
            current_area.have_inspected_objects(True)

            if current_objects:
                print("Around you, you can see a:",current_objects[0].name + \
                      "".join([", "+i.name for i in current_objects[1:]]))
            else:
                print("There're no objects in this area!")

            print()
            continue

        if input_choice == "status":
            main_char.get_update()
            print()
            continue

        if input_choice == "help":
            world_help(commands)
            print()
            continue

        if input_choice == "save":
            save_game(saved_data)
            print()
            continue

        if input_choice == "be a dev":
            main_char.is_dev(True)
            commands.remove("be a dev")
            all_possible_inputs.remove("be a dev")
            commands += ["add","die"]
            all_possible_inputs += ["add " + i for i in ("area","object")] + ["die"]

            if saved_data["difficulty"] == "Hard":
                commands += ["teleport"]
                all_possible_inputs += ["teleport"]

            continue

        if main_char.is_dev():
            if input_choice == "add area":
                while True:
                    print("Input the coordinates you want to add the area to: ")
                    current_coord = check_user_input_coords()

                    if not current_coord:
                        break

                    print("Select the events you want the area to have, continuing\n"+\
                          "by inputting nothing:\n")

                    input_choices = list(world.get_default_events().keys())
                    events = []

                    while True:
                        input_choice = check_input(*input_choices,invis_choices = [""], back = True)

                        if input_choice in ("","back"):
                            break

                        events.append(input_choices[input_choice])
                        del input_choices[input_choice]

                    if input_choice == "back":
                        continue

                    create_area(world,current_coord,events,True)
                    print("Area created!\n")
                    break

                continue

            if input_choice == "add object":
                import item_list

                item_choices = {"item_object":[],"item_name":[]}

                for item_object in item_list.item_object_list:
                    item_choices["item_object"].append(item_object)
                    item_choices["item_name"].append(item_object().name)

                item_choices["item_object"] += [gold,shop]
                item_choices["item_name"] += [gold().name,shop(main_char).name]

                for i in load_chars("enemies"):
                    item_choices["item_object"].append(spawn_character(i))
                    item_choices["item_name"].append(spawn_character(i)().name)

                for i in load_chars():
                    item_choices["item_object"].append(spawn_character(i))
                    item_choices["item_name"].append(spawn_character(i)().name)

                while True:
                    input_choice = check_input(*item_choices["item_name"],back = True)

                    if input_choice == "back":
                        break

                    input_item = item_choices["item_object"][input_choice]
                    print("Input the amount:")

                    while True:
                        try:
                            input_amount = int(input("> "))
                        except ValueError:
                            print("You must input an integer value!")
                            continue
                        finally:
                            print()

                        break

                    try:
                        input_item(current_level = 0)
                    except TypeError:
                        if input_item().name == "Gold":
                            current_area.add_object(input_item(input_amount))

                            continue

                        try:
                            input_item().type
                        except AttributeError:
                            for i in range(input_amount):
                                current_area.add_object(input_item())
                        else:
                            print("Do you want to add it as ally or enemy?\n")
                            input_choices = ("Ally","Enemy")
                            input_choice = check_input(*input_choices)
                            input_choice = input_choices[input_choice]

                            for i in range(input_amount):
                                if input_choice == "Ally":
                                    current_area.add_ally(input_item())
                                    continue

                                current_area.add_enemy(input_item())

                        continue
                    else:
                        print("Input the object's level, with level 0 being the base amount.")

                        while True:
                            try:
                                input_choice = int(input("> "))
                            except ValueError:
                                print("You must input an integer value!")
                                continue
                            finally:
                                print()

                            if input_choice < 0:
                                print("Cannot input negative numbers!")
                                continue

                            current_level = input_choice
                            break


                    try:
                        input_item(main_char,current_level)
                    except TypeError:
                        pass
                    else:
                        for i in range(input_amount):
                            current_area.add_object(input_item(main_char,current_level))

                        continue

                    try:
                        input_item().type
                    except AttributeError:
                        for i in range(input_amount):
                            current_area.add_object(input_item(current_level))
                    else:
                        print("Do you want to add it as ally or enemy?\n")
                        input_choices = ("Ally","Enemy")
                        input_choice = check_input(*input_choices)
                        input_choice = input_choices[input_choice]

                        for i in range(input_amount):
                            if input_choice == "Ally":
                                current_area.add_ally(input_item(current_level))
                                continue

                            current_area.add_enemy(input_item(current_level))

                continue

            if input_choice == "die":
                return "User_lost"

        try:
            int(input_choice)
        except ValueError:
            event = input_choice[len("move "):]
        else:
            object_list = current_area.get_objects()

            if num_choices[input_choice] != "Grab all items.":
                object_list = [object_list[input_choice]]

                if object_list[0].name == "Shop":
                    object_list[0].get_shop()
                    continue

            i = len(object_list)-1

            while i >= 0:
                item_object = object_list[i]

                if item_object.name != "Shop":
                    if item_object.name == "Gold":
                        main_char.get_inventory().add_gold(item_object.amount)
                        print("You have received {} Gold!".format(item_object.amount))
                        current_area.remove_object(item_object)
                    elif main_char.get_inventory().add_item(item_object) is not None:
                        current_area.remove_object(item_object)
                        print("The {} has been added to the inventory!".format(item_object.name))

                i -= 1

            print()
            continue

        if world.safe_event() != event:
            enemy_units = current_area.get_enemies()

            if enemy_units:
                allied_units = current_area.get_allies()
                # Temporary adding main char to the allies list
                allied_units.insert(0,main_char)

                if enemy_units[0].name == "Final Boss":
                    print("You try to leave the area, however there's a weird wind and weird\n"+\
                          "flowers start raining down. You start seeing something in the distance...\n"+\
                          "I..t's... yo..u?")
                    import pickle
                    enemy_units[0] = pickle.loads(pickle.dumps(main_char))

                    try:
                        combat_result = combat(allied_units,enemy_units, final_boss = True)
                    finally:
                        allied_units.remove(main_char)

                    if combat_result == "User_lost":
                        return "User_lost"

                    if combat_result == "User_won":
                        print("You end the fight, however, you're on the ground, as if\n"+\
                              "you had just woken up. It might have been a dream you think,\n"+\
                              "or was it?")
                        world.has_beaten_final_boss(True)
                else:
                    print("You got ambushed! To continue the path you must kill all enemies!")

                    try:
                        combat_result = combat(allied_units,enemy_units)
                    finally:
                        allied_units.remove(main_char)

                    if combat_result == "User_left_combat":
                        print("You returned to the area.\n")
                        continue

                    if combat_result == "User_lost":
                        return "User_lost"

                    if combat_result == "User_won":
                        print("You moved to the next area!")

        try:
            current_coord = world.get_event_consequence(event)
        except KeyError:
            if saved_data["difficulty"] == "Hard":
                maximum = 101
                minimum = 10
            else:
                maximum = 11
                minimum = 1

            current_coord = world.get_new_coords(current_area.coord,[event],\
                                                 delta = random.randrange(minimum,maximum))[event]
            world.has_shop_been_found(False)
            creating_unknown_area = True
        else:
            creating_unknown_area = False

        old_area = current_area
        world.change_current_area(current_coord)

        try:
            current_area = world.get_area(current_coord)
        except KeyError:
            if saved_data["difficulty"] == "Hard":
                events = []
            else:
                events = list(world.get_default_events().keys())

                if saved_data["difficulty"] == "Normal":
                    for i in range(4):
                        if random.randrange(4) > 0:
                            events.remove(random.choice(events))

            create_area(world,current_coord,events,creating_unknown_area)
            current_area = world.get_area()
            current_level = world.get_level()

            import item_list

            for i in item_list.item_object_list:
                try:
                    item = i(current_level)
                except TypeError:
                    item = i()

                try:
                    item.consumable
                except AttributeError:
                    chance = 5
                else:
                    chance = 10

                if saved_data["difficulty"] == "Easy":
                    chance *= 2
                elif saved_data["difficulty"] == "Hard":
                    chance *= 0

                if random.randrange(100) < chance:
                    current_area.add_object(item)

            if random.randrange(10) < 3:
                if saved_data["difficulty"] == "Easy":
                    maximum = 500
                elif saved_data["difficulty"] == "Hard":
                    maximum = 100
                else:
                    maximum = 250

                current_area.add_object(gold(random.randrange(50,maximum,50)))

            shop_times = 5
            enemy_chance = 4
            enemy_count = 5

            if saved_data["difficulty"] == "Easy":
                shop_times = 3
                enemy_count = 3
            elif saved_data["difficulty"] == "Hard":
                shop_times = 10
                enemy_chance = 7
                enemy_count = 10

            if not world.has_beaten_final_boss() and current_level % 10 == 0:
                current_area.add_enemy(final_boss_object())
            elif current_level % shop_times == 0:
                current_area.add_object(shop(main_char,current_level))
            elif random.randrange(10) < enemy_chance:
                for char in load_chars("enemies"):
                    if char == "big_unit":
                        enemy_count //= 3

                    for i in range(random.randrange(enemy_count)):
                        current_area.add_enemy(spawn_character(char)(current_level))
        else:
            if not creating_unknown_area:
                path_index = world.get_path_indexes(old_area.coord,current_coord)

                if path_index[0] != path_index[1]:
                    world.combine_paths(path_index)

        world.safe_event(world.get_default_events()[event])

    return None

def main():
    """Main function."""
    welcome()
    player_scores = load("leaderboards.txt")
    print()

    while True:
        input_choices = ("Start Game","Leaderboards")
        input_choice = check_input(*input_choices, vis_choices = {"X":"Quit"},quitting = False)
        # Adding X:Quit as vis_choices so to not trigger the request for saving
        # which otherwise exists everywhere else the function is used.

        if input_choice == "X":
            print("Goodbye!",end="")
            input()
            sys.exit()

        input_choice = input_choices[input_choice]

        if input_choice == "Start Game":
            saved_files = load("saved_game_file_names.txt",[])

            while True:
                if saved_files:
                    input_choices = ("Load Game","New Game")
                    input_choice = check_input(*input_choices,back = True, quitting = False)

                    if input_choice == "back":
                        break

                    input_choice = input_choices[input_choice]

                    if input_choice == "Load Game":
                        while True:
                            if not saved_files:
                                break

                            string = []

                            for i in saved_files:
                                data = load(i)
                                string.append(("Saved file name: {}\nUser Name: "+\
                                              "{}\nDifficulty: {}")\
                                              .format(i,data["user_name"],data["difficulty"]))

                            print("\n\n".join(string))
                            input_choices = ("Run","Delete")
                            print()
                            input_choice = check_input(*input_choices,back = True, quitting = False)

                            if input_choice == "back":
                                break

                            input_choice = input_choices[input_choice]

                            while True:
                                saved_data_inputs = []

                                for index,i in enumerate(saved_files):
                                    data = load(i)
                                    saved_data_inputs.append((str(index)+".Saved file name: "+\
                                                              "{}\nUser Name: {}\nDifficulty: {}")\
                                                          .format(i,data["user_name"],data["difficulty"]))

                                if input_choice == "Run":
                                    print("Choose a saved file to run:")
                                else:
                                    print("Choose a saved file to delete:")

                                print()
                                print("\n\n".join(saved_data_inputs))
                                print()
                                saved_file = check_input(invis_choices = range(len(saved_files))\
                                                         ,back = True, quitting = False)

                                if saved_file == "back":
                                    break

                                if input_choice == "Run":
                                    saved_file = saved_files[saved_file]
                                    saved_data = load(saved_file)
                                    saved_data["saved_file"] = saved_file
                                    break

                                import os # putting it here for performance
                                os.remove(saved_files[saved_file])
                                del saved_files[saved_file]
                                save(saved_files,"saved_game_file_names.txt")

                                if not saved_files:
                                    print("All saved files have been deleted!")
                                    break

                            if saved_file == "back":
                                continue

                            break

                        if not saved_files:
                            break

                        if input_choice == "back":
                            continue

                if not saved_files or input_choice == "New Game":
                    print("Input your name (this will be used later on if you decide to\n"+\
                      "add your score to the leaderboards.)")
                    input_name = input("> ")
                    print()
                    print("Choose a difficulty:\n")
                    input_choices = ("Easy","Normal","Hard")
                    input_difficulty = check_input(*input_choices,back = True, quitting = False)

                    if input_difficulty == "back":
                        if saved_files:
                            continue

                        break

                    input_difficulty = input_choices[input_difficulty]
                    saved_data = {"difficulty":input_difficulty,"user_name":input_name,"objects":{}}
                    import datetime #putting it here for performance
                    date = datetime.datetime.now()
                    file_name = "{}_{}_{}_{}_{}_{}.txt"\
                                .format(date.year, date.month, date.day, date.hour, date.minute, date.second)
                    saved_files.append(file_name)
                    save(saved_files,"saved_game_file_names.txt")
                    saved_data["saved_file"] = file_name
                    save(saved_data,file_name)

                try:
                    result = main_game(saved_data)
                except exceptions.UserExit:
                    print("Do you want to save first before exiting?\n")
                    input_choice = check_input(vis_choices = {"Y":"Yes","N":"No"}, quitting = False)

                    if input_choice == "Y":
                        save_game(saved_data)

                    print("Goodbye!",end="")
                    input()
                    sys.exit()
                else:
                    if result == "User_lost":
                        print("You're dead...")
                        area_count = saved_data["objects"]["world"].area_count
                        difficulty = saved_data["difficulty"]
                        print("You have found {} areas on a {} difficulty, getting a score of: "\
                              .format(area_count,difficulty),end="")

                        if difficulty == "Easy":
                            difficulty = 1
                        elif difficulty == "Normal":
                            difficulty = 5
                        elif difficulty == "Hard":
                            difficulty = 10

                        score = area_count*difficulty
                        print(score)
                        previous_score = player_scores.get(saved_data["user_name"])

                        if previous_score:
                            print("Your previous score was: {}".format(previous_score))

                        if not previous_score or previous_score > score:
                            print("Do you want to save it to the leaderboards?\n")
                            input_choice = check_input(vis_choices = {"Y":"Yes","N":"No"}, quitting = False)

                            if input_choice == "Y":
                                player_scores[saved_data["user_name"]] = score
                                save(player_scores,"leaderboards.txt")
                                print("Successfully saved!")

                break

            continue

        if input_choice == "Leaderboards":
            if player_scores:
                leaderboards(player_scores)
            else:
                print("There's no one in the leaderboards. Be the first!")

            print()
            continue

# Driver function for the program
if __name__ == "__main__":
    main()
