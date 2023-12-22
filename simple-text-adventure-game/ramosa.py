import random
import buff_list
from buff import buff
from events import events
from exceptions import AbilityError

class Character(buff,events):
    def __init__(self):
        self.type = "Character"
        self.name = "Ramosa"
        self.hp = 700
        self.mana = 500
        self.dmg = 50
        self.mana_regen = 30
        self.gold = 1000
        self.abilities_dict = {"Q":"Stay still!", "W":"Rise!", "E":"Come to me..."}
        buff.__init__(self)
        events.__init__(self)

    class __Stay_still():
        def __init__(ability,self):
            ability.affects = "aoe_enemy"
            ability.dmg = self.dmg*0.7
            ability.description = "Deals damage to all enemies with a chance of applying\n"+\
                                  "'Stay Still' to them."
            ability.mana = 200
            ability.buff_class = buff_list.Stay_still
            ability.rounds = 2

        def trigger(ability,target):
            """Triggers the ability on the 'target' object.
                Args:
                        target (object): an object of a character class
            """
            target.receive_damage(ability.dmg)

            if random.randrange(10) < 6:
                target.grant_temp_buff(ability.buff_class(),ability.rounds)

    class __Rise():
        def __init__(ability,self,**kwargs):
            ability.affects = "self"
            ability.description = "Summons a small unit which randomly attacks enemies each turn."
            ability.mana = 300

            if kwargs:
                ability.__all_units = kwargs["all_units"]

        def trigger(ability,self):
            """Triggers the ability."""
            for team in ability.__all_units:
                if self in team:
                    import small_unit
                    team.append(small_unit.Character())
                    return

    class __Come_to_me():
        def __init__(ability,self,**kwargs):
            ability.affects = "enemy"
            ability.description = ("Takes control of an enemy for the entirety of this area.\n"+\
                                   "Once all enemies are killed, it returns to the enemy team.")
            ability.mana = 500

            if kwargs:
                for team_index, team in enumerate(kwargs["all_units"]):
                    if self in team:
                        if len(kwargs["all_units"][abs(team_index-1)]) == 1:
                            raise AbilityError("Cannot cast while there's only one enemy remaining!")

                        break

                ability.__all_units = kwargs["all_units"]

        def trigger(ability,target):
            """Triggers the ability on the 'target' object.
                Args:
                        target (object): an object of a character class
            """
            for team_index, team in enumerate(ability.__all_units):
                if target in team:
                    team.remove(target)
                    ability.__all_units[abs(team_index-1)].append(target)
                    break

            target.is_controlled = True

    def Q(self):
        """Wrapper for the ability class.
        Returns:
                class: the ability class
        """
        return self.__Stay_still

    def W(self):
        """Wrapper for the ability class.
        Returns:
                class: the ability class
        """
        return self.__Rise

    def E(self):
        """Wrapper for the ability class.
        Returns:
                class: the ability class
        """
        return self.__Come_to_me
