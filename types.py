from color import Color


class Types(Enum):
    """Enumeration for Pokemon types"""
    FIRE = "fire"
    WATER = "water"
    GRASS = "grass"
    ELECTRIC = "electric"
    NORMAL = "normal"
    STEEL = "steel"
    FIGHTING = "fighting"
    STONE = "stone"
    FAIRY = "fairy"
    DRAGON = "dragon"
    DARK  = "dark"
    GHOST = "ghost"
    PSYCHIC = "psychic"
    GROUND = "ground"
    FLYING = "flying"
    POISON = "poison"
    ICE = "ice"
    INSECT = "insect"

class Type:
    """Class representing a Pokemon type"""
    def __init__(self, type : Types, color : Color):
        self.__type = type
        self.__color = color

    def get_type(self) -> Types:
        return self.__type

    def get_color(self) -> Color:
        return self.__color