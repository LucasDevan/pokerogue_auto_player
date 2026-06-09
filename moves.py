from types import Types

class Move:
    """Class representing a Pokemon move"""
    def __init__(self, name, move_type : Types, power):
        self.__name = name
        self.__move_type = move_type
        self.__power = power

    def get_name(self):
        return self.__name
    
    def get_type(self):
        return self.__move_type
    
    def get_power(self):
        return self.__power
 