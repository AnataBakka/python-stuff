class Ill_never_yield():
    def __init__(self):
        self.name = "I'll never yield!"

    def passive(self,target):
        """Triggers the buff on the 'target' object.
            Args:
                    target (object): an object of a character class
        """
        target.shield_increase(200,buff_type = "temp")

class Stay_still():
    def __init__(self):
        self.name = "Stay still!"

    def passive(self,target):
        """Triggers the buff on the 'target' object.
            Args:
                    target (object): an object of a character class
        """
        target.temp["cannot_act"]["temp"] = True

def get_description():
    """Returns a dictionary of descriptions, pointed by the buff class.
        Returns:
                dictionary: class:description
    """
    return{"I'll never yield!":"Grants a shield.",
           "Stay still!":"Affected unit cannot act in their turn."
        }
