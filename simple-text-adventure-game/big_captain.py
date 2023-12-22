from buff import buff
from events import events
import buff_list

class Character(buff,events):
    def __init__(self):
        self.type = "Character"
        self.name = "Big Captain"
        self.hp = 1000
        self.mana = 400
        self.dmg = 100
        self.mana_regen = 30
        self.gold = 1000
        self.abilities_dict = {"Q":"Overpowered Slam", "W":"I'll never yield!", "E":"Get Dunked"}
        buff.__init__(self)
        events.__init__(self)

    class __Overpowered_Slam():
        def __init__(ability,self):
            ability.affects = "aoe_enemy"
            ability.dmg = self.dmg
            ability.description = "Deals damage to all enemies."
            ability.mana = 100

        def trigger(ability,target):
            """Triggers the ability on the 'target' object.
                Args:
                        target (object): an object of a character class
            """
            target.receive_damage(ability.dmg)

    class __Ill_never_yield():
        def __init__(ability):
            ability.affects = "self"
            ability.mana = 200
            ability.rounds = 3
            ability.buff_class = buff_list.Ill_never_yield

        def trigger(ability,target):
            """Triggers the ability on the 'target' object.
                Args:
                        target (object): an object of a character class
            """
            target.grant_temp_buff(ability.buff_class(),ability.rounds)

    class __Get_Dunked():
        def __init__(ability,self):
            ability.affects = "enemy"
            ability.dmg = self.dmg*5
            ability.mana = 400
            ability.description = "Deal high amount of damage to a single enemy."

        def trigger(ability,target):
            """Triggers the ability on the 'target' object.
                Args:
                        target (object): an object of a character class
            """
            target.receive_damage(ability.dmg)

    def Q(self):
        """Wrapper for the ability class.
            Returns:
                    class: the ability class
        """
        return self.__Overpowered_Slam

    def W(self):
        """Wrapper for the ability class.
            Returns:
                    class: the ability class
        """
        return self.__Ill_never_yield

    def E(self):
        """Wrapper for the ability class.
            Returns:
                    class: the ability class
        """
        return self.__Get_Dunked
