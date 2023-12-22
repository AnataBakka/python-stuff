import random
from exceptions import AbilityError

class events():
    def __init__(self):
        self.current_hp = self.hp
        self.current_mana = self.mana

    def receive_damage(self,dmg):
        """Used for dealing damage to a character object.
            Args:
                    dmg (number): amount of damage received
        """
        while True:
            if self.shield:
                self.shield -= dmg

                if self.shield <= 0:
                    print("{} has blocked {:.0f} dmg.".format(self.name,dmg + self.shield)+\
                          "\nThe shield has been destroyed.")

                    if self.shield < 0:
                        dmg = -self.shield
                        self.shield = 0
                        continue
                else:
                    print("{} has blocked {:.0f} dmg.".format(self.name,dmg))
            else:
                self.current_hp -= dmg
                print("{} has received {:.0f} dmg.".format(self.name,dmg))

            break

    def check_hp_status(self):
        """Returns 'CharacterDead' if the character's hp is below 0, \
else it returns None.
            Returns:
                    string: if character is dead
        """
        if self.current_hp <= 0:
            return "CharacterDead"

        return None

    def round_events(self):
        """Triggers the round events (used while in combat)."""
        self.remove_temp_buffs()
        self.current_mana += self.mana_regen

        if self.current_mana > self.mana:
            self.current_mana = self.mana

    class Normal_Attack():
        def __init__(ability,self,**kwargs):
            if kwargs.get("affects"):
                ability.affects = kwargs["affects"]
            else:
                ability.affects = "enemy"

            if kwargs.get("dmg"):
                ability.dmg = kwargs["dmg"]
            else:
                ability.dmg = self.dmg*0.3

            if kwargs.get("mana"):
                ability.mana = kwargs["mana"]
            else:
                ability.mana = 0

        def trigger(ability,target):
            """Triggers the ability on the 'target' object.
                Args:
                        target (object): an object of a character class
            """
            target.receive_damage(ability.dmg)

    def A(self):
        """Wrapper for the normal attack class.
            Returns:
                    class: normal attack class
        """
        return self.Normal_Attack

    def get_update(self):
        """Prings the stats of the character."""
        string_print = ""

        if self.cannot_act:
            string_print += "(Stunned) "

        string_print += ("{name}\n hp = {current_hp:<5.0f} / {max_hp:<15.0f}"+\
                       "mana = {current_mana:<5.0f} / {max_mana:<15.0f}"+\
                         "dmg = {dmg:.0f}\n").format(\
                           name = self.name, current_hp = self.current_hp,\
                           max_hp = self.hp, current_mana = self.current_mana,\
                           max_mana = self.mana, dmg = self.dmg)

        if self.shield:
            string_print += "shield = {shield:.0f}\n".format(shield = self.shield)

        print(string_print)

    def get_abilities(self):
        """Returns a dictionary of the character's abilities.
            Returns:
                    dictionary: character abilities
        """
        return self.abilities_dict

    def use_ability(self,ability_key,**kwargs):
        """Checks if the ability can be cast and if it can it's returned.
            Args:
                    ability_key (string): key of the ability 'Q','W','E'
                    kwargs: additional paramaters to be given to the ability
            Returns:
                    object: object of the ability key
            Raises:
                    AbilityError: if the ability cannot be cast.
        """
        if ability_key == "A":
            ability = self.A()
        elif ability_key == "Q":
            ability = self.Q()
        elif ability_key == "W":
            ability = self.W()
        elif ability_key == "E":
            ability = self.E()

        try:
            ability = ability(self,**kwargs)
        except TypeError:
            try:
                ability = ability(self)
            except TypeError:
                try:
                    ability = ability()
                except TypeError:
                    pass

        if self.current_mana < ability.mana:
            raise AbilityError("You don't have mana for that ability!")

        return ability

    def random_ability(self, **kwargs):
        """Returns a random ability that can be cast.
            Args:
                    kwargs: additional paramaters to be given to the ability
            Returns:
                    object: ability object
        """
        ability_list = []

        for i in ["A","Q","W","E"]:
            try:
                ability = self.use_ability(i,**kwargs)
            except AbilityError:
                continue

            ability_list.append(i)

        ability = self.use_ability(random.choice(ability_list), **kwargs)
        self.current_mana -= ability.mana
        return ability

    def add_inventory(self,inventory_object):
        """Adds an inventory object to an attribute.
            Args:
                    inventory_object (object): object of an inventory
        """
        self.__inventory = inventory_object

    def get_inventory(self):
        """Returns the inventory object.
            Returns:
                    object: inventory
        """
        return self.__inventory

    def is_dev(self,boolean = "get"):
        """Used for adding a boolean value to an attribute and further checking \
that value with the value 'get' of the same 'boolean' paramater.
            Args:
                    boolean (string / boolean): 'get' / boolean
            Returns:
                    boolean: only if 'boolean' is 'get'
        """
        if boolean == "get":
            return self.__is_dev

        self.__is_dev = boolean
        return None
