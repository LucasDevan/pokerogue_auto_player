from enum import Enum
from moves import Move
from types import Types

class PokemonStatus(Enum):
    """Enumeration for Pokemon status"""
    POISSONED = "poissoned"
    PARALYZED = "paralyzed"
    SLEEPING = "sleeping"
    NONE = "NONE"

class Pokemon:
    """Class representing a Pokemon"""
    def __init__(self, name : str, pokemon_type_1 : Types, pokemon_type_2 : Types, hp : int, attack : int, defence : int, special_attack : int, special_defence : int, speed : int, moves : tuple, status : PokemonStatus = PokemonStatus.NONE):
        self.__name = name
        self.__type_1 = pokemon_type_1
        self.__type_2 = pokemon_type_2  
        self.__max_hp = hp
        self.__attack = attack
        self.__special_attack =  special_attack
        self.__special_defence = special_defence
        self.__defence = defence
        self.__speed =speed
        if(len(moves) > 4):
            moves = {moves[0],moves[1],moves[2],moves[3]}
        self.__moves = moves
        self.__status = status
        self.__is_confused = False

    def get_name(self) -> str:
        return self.__name
    
    def get_types(self) -> tuple:
        return (self.__type_1, self.__type_2)
    
    def get_type_1(self) -> Types:
        return self.__type_1
    
    def get_type_2(self) -> Types:
        return self.__type_2
    
    def get_hp(self) -> int:
        return self.__max_hp
    
    def get_moves(self) -> tuple:
        return self.__moves
    
    def get_move(self,index : int) -> Move:
        return self.__moves[index]
    
    def get_attack(self) -> int:
        return self.__attack
    
    def get_defence(self) -> int:
        return self.__defence
    
    def get_special_attack(self) -> int: 
        return self.__special_attack
    
    def get_special_defence(self) -> int:
        return self.__special_defence
    
    def get_speed(self) -> int:
        return self.__speed
    
    def get_status(self) -> PokemonStatus:
        return self.__status
    
    def is_confused(self) -> bool:
        return self.__is_confused
    
    def set_is_confused(self, confused : bool):
        self.__is_confused = confused
    
    def set_status(self, status : PokemonStatus):
        self.__status = status

    def level_up(self,hp_increase = 0, attack_increase = 0, defence_increase = 0, special_attack_increase = 0, special_defence_increase = 0, speed_increase = 0):
        self.__max_hp += hp_increase
        self.__attack += attack_increase
        self.__defence += defence_increase
        self.__special_attack += special_attack_increase
        self.__special_defence += special_defence_increase
        self.__speed += speed_increase 