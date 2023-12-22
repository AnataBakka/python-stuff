from buff import buff
from events import events

class Character(buff,events):
    def __init__(self,current_level = 0):
        current_level //= 5
        self.type = "Character"
        self.name = "Big Unit"
        self.hp = 700+200*current_level
        self.mana = 100
        self.dmg = 100+30*current_level
        self.mana_regen = 30
        self.gold = 100+50*current_level
        buff.__init__(self)
        events.__init__(self)

    def Q(self):
        """Wrapper for the ability object.
        Returns:
                object: ability object
        """
        return self.Normal_Attack(self,affects = "aoe_enemy",dmg = self.dmg*1.5, mana = 100)

    def W(self):
        """Wrapper for the ability object.
        Returns:
                object: ability object
        """
        return self.Normal_Attack(self,affects = "aoe_enemy",dmg = self.dmg*1.7, mana = 100)

    def E(self):
        """Wrapper for the ability object.
        Returns:
                object: ability object
        """
        return self.Normal_Attack(self,affects = "aoe_enemy",dmg = self.dmg*2, mana = 100)
