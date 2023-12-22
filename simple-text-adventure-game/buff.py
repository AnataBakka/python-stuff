class buff():
    def __init__(self):
        self.temp_buffs = {}
        self.permanent_buffs = []
        self.shield = 0
        self.temp = {}
        self.buff_defaults = {"hp":0,"mana":0,"shield":0,"dmg":0,\
                              "cannot_act": False}
        self.cannot_act = False
        self.is_controlled = False

        for buff_type,default in self.buff_defaults.items():
            self.temp[buff_type] = {"permanent":default,"temp":default}

    def grant_permanent_buff(self,buff_object):
        """Puts the buff_object in the permanent buff list.
            Args:
                    buff_object (object): object of a buff
        """
        self.permanent_buffs.append(buff_object)
        self.update_buffs("permanent")

    def grant_temp_buff(self,buff_object,rounds = 1):
        """Puts the buff_object in the temporary buff dictionary.
            Args:
                    buff_object (object): object of a buff
                    rounds (number): amount of rounds the buff should be kept \
                    defaulting to 1 round
        """
        print("{} has been granted {} for {} rounds.".format(self.name,buff_object.name,rounds))
        self.temp_buffs[buff_object] = rounds
        self.update_buffs("temp")

    def remove_temp_buffs(self):
        """Removes 1 round from each buff object in the temporary buff list. \
If it reaches 0 rounds the buff object is completely removed."""
        buffs_to_remove = []

        for buff_object in self.temp_buffs:
            self.temp_buffs[buff_object] -= 1

            if self.temp_buffs[buff_object] == 0:
                buffs_to_remove.append(buff_object)

        for buff_object in buffs_to_remove:
            print("{} has been removed from {}.".format(buff_object.name,self.name))
            self.temp_buffs.pop(buff_object)

        if buffs_to_remove:
            self.update_buffs("temp")

    def remove_permanent_buff(self,buff_object):
        """Removes a permanent buff object from the permanent buff list.
            Args:
                    buff_object (object): object of a buff
        """
        self.permanent_buffs.remove(buff_object)
        self.update_buffs("permanent")

    def update_buffs(self,update = "temp"):
        """Updates the effects of the type 'update' buffs.
            Args:
                    update (string): 'temp' / 'permanent'
        """
        args = ["temp","permanent"]

        if update == "permanent":
            args[0],args[1] = args[1],args[0]

        pre_temp = {}

        for buff_type,default in self.buff_defaults.items():
            pre_temp[buff_type] = self.temp[buff_type][args[0]]
            self.temp[buff_type][args[0]] = default

        if update == "temp":
            for buff_object in self.temp_buffs:
                buff_object.passive(self)
        else:
            for buff_object in self.permanent_buffs:
                buff_object.passive(self)

        if self.temp["shield"][args[0]] > pre_temp["shield"]:
            self.shield += self.temp["shield"][args[0]] - pre_temp["shield"]
        elif self.temp["shield"][args[0]] + self.temp["shield"][args[1]] < self.shield:
            self.shield = self.temp["shield"][args[0]] + self.temp["shield"][args[1]]

        self.hp += self.temp["hp"][args[0]] - pre_temp["hp"]
        self.current_hp += self.temp["hp"][args[0]] - pre_temp["hp"]
        self.mana += self.temp["mana"][args[0]] - pre_temp["mana"]
        self.current_mana += self.temp["mana"][args[0]] - pre_temp["mana"]
        self.dmg += self.temp["dmg"][args[0]] - pre_temp["dmg"]

        if self.temp["cannot_act"][args[0]] or self.temp["cannot_act"][args[1]]:
            self.cannot_act = True
        else:
            self.cannot_act = False

    def get_buffs(self):
        """Returns the temporary buff dictionary.
            Returns:
                    dictionary: temporary buff dictionary
        """
        return self.temp_buffs

    def hp_increase(self,amount,buff_type = None):
        """A buff that increases hp based on 'buff type'.
            Args:
                    amount (number): amount of hp to increase
                    buff_type (string): 'temp' / 'permanent' or if not given, \
                    instant.
        """
        if buff_type:
            self.temp["hp"][buff_type] += amount
        else:
            self.current_hp += amount

            if self.current_hp > self.hp:
                self.current_hp = self.hp

    def mana_increase(self,amount,buff_type = None):
        """A buff that increases mana based on 'buff type'.
            Args:
                    amount (number): amount of mana to increase
                    buff_type (string): 'temp' / 'permanent' or if not given, \
                    instant.
        """
        if buff_type:
            self.temp["mana"][buff_type] += amount
        else:
            self.current_mana += amount

            if self.current_mana > self.mana:
                self.current_mana = self.mana

    def shield_increase(self,amount,buff_type = None):
        """A buff that increases shield based on 'buff type'.
            Args:
                    amount (number): amount of shield to increase
                    buff_type (string): 'temp' / 'permanent'
        """
        if buff_type:
            self.temp["shield"][buff_type] += amount

    def dmg_increase(self,amount,buff_type = None):
        """A buff that increases dmg based on 'buff type'.
            Args:
                    amount (number): amount of dmg to increase
                    buff_type (string): 'temp' / 'permanent'
        """
        if buff_type:
            self.temp["dmg"][buff_type] += amount
