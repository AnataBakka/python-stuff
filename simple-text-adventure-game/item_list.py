from exceptions import ItemError

class hp_potion():
    def __init__(self):
        self.consumable = True
        self.name = "Health Potion"
        self.cost = 50
        self.__hp_increase = 100
        self.description = "Regenerate {} health.".format(self.__hp_increase)

    def active(self,target):
        """Triggers the buff on the 'target' object.
            Args:
                    target (object): an object of a character class
            Raises:
                    ItemError: if target's hp is at maximum
        """
        if target.current_hp == target.hp:
            raise ItemError("Cannot consume if health is at maximum!")

        target.hp_increase(self.__hp_increase)

class mana_potion():
    def __init__(self):
        self.consumable = True
        self.name = "Mana Potion"
        self.cost = 50
        self.__mana_increase = 50
        self.description = "Regenerate {} mana.".format(self.__mana_increase)

    def active(self,target):
        """Triggers the buff on the 'target' object.
            Args:
                    target (object): an object of a character class
            Raises:
                    ItemError: if target's mana is at maximum
        """
        if target.current_mana == target.mana:
            raise ItemError("Cannot consume if mana is at maximum!")

        target.mana_increase(self.__mana_increase)

class weapon():
    def __init__(self,current_level = 0):
        current_level = current_level // 5 + 1
        self.name = "Weapon"
        self.cost = 200*current_level
        self.__dmg_increase = current_level*10
        self.description = "Increase your dmg by {}.".format(self.__dmg_increase)

    def passive(self,target):
        """Triggers the buff on the 'target' object.
            Args:
                    target (object): an object of a character class
        """
        target.dmg_increase(self.__dmg_increase,buff_type = "permanent")

class armor():
    def __init__(self,current_level = 0):
        current_level = current_level //5 + 1
        self.name = "Armor"
        self.cost = 300*current_level
        self.__hp_increase = current_level*50
        self.description = "Increase your current health and health cap by {}.".format(self.__hp_increase)

    def passive(self,target):
        """Triggers the buff on the 'target' object.
            Args:
                    target (object): an object of a character class
        """
        target.hp_increase(self.__hp_increase,buff_type = "permanent")

item_object_list = [hp_potion,mana_potion,weapon,armor]
