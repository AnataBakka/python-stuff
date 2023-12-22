from buff import buff
from events import events

class Character(buff,events):
    def __init__(self,current_level = 0):
        current_level //= 5
        self.type = "Character"
        self.name = "Small Unit"
        self.hp = 300+100*current_level
        self.mana = 100
        self.dmg = 50+20*current_level
        self.mana_regen = 30
        self.gold = 50+10*current_level
        buff.__init__(self)
        events.__init__(self)

    def Q(self):
        """Wrapper for the ability object.
        Returns:
                object: ability object
        """
        return self.Normal_Attack(self,dmg = self.dmg*0.7, mana = 100)

    def W(self):
        """Wrapper for the ability object.
        Returns:
                object: ability object
        """
        return self.Normal_Attack(self,dmg = self.dmg*0.8, mana = 100)

    def E(self):
        """Wrapper for the ability object.
        Returns:
                object: ability object
        """
        return self.Normal_Attack(self,dmg = self.dmg*0.9, mana = 100)
