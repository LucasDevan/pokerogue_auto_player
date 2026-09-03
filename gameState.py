from enum import Enum

class GameState(Enum):
    """Enumeration for possible game states"""
    MENU = "menu"
    BATTLE = "battle"
    DOUBLE_BATTLE = "double battle",
    MENU_KO = "menu ko"
    UNKNOWN = "unknown"
    SHOP = "shop"
    EVOLUTION = "evolution",
    LEARNING_MOVE = "learning move",
    MAIN_TITLE = "main title"