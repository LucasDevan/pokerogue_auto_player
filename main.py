"""
Very simple Pokerogue auto-battler prototype.

Features:
- Toggle bot ON with F8
- Pause bot with ESC
- Quit completely with F9
- Detects rough game states using pixel colors
- Sends Enter automatically
- Uses mock/example pixel values

Requirements:
pip install pyautogui pynput pillow
"""

import time
import pyautogui
from pynput import keyboard
from enum import Enum

# =========================
# CONFIG
# =========================


class PokemonStatus(Enum):
    """Enumeration for Pokemon status"""
    POISSONED = "poissoned"
    PARALYZED = "paralyzed"
    SLEEPING = "sleeping"
    NONE = "NONE"

class GameState(Enum):
    """Enumeration for possible game states"""
    MENU = "menu"
    BATTLE = "battle"
    MENU_KO = "menu ko"
    UNKNOWN = "unknown"

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

class Move:
    """Class representing a Pokemon move"""
    def __init__(self, name, move_type, power):
        self.__name = name
        self.__move_type = move_type
        self.__power = power

    def get_name(self):
        return self.__name
    
    def get_type(self):
        return self.__move_type
    
    def get_power(self):
        return self.__power
    
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

SCAN_INTERVAL = 0.5

# Example coordinates/colors
# You MUST adapt these to your setup
# Format: (x, y, width, height) - defines a region to sample from

# Regions to check (top-left corner + size)
REGION_BOX_BATTLE = (2417, 1224, 20, 20)
REGION_BOX_MENU = (140, 120, 20, 20)
REGION_POKEMON_1_MENU = (564, 429, 30, 30)
REGION_POKEMON_2_MENU = (600, 900, 30, 30)
REGION_MONEY = (656, 976, 30, 30)

# RGB reference values - now as lists of target colors
MENU_BACKGROUND_COLORS = [(16, 24, 32)]
BOX_OUTLINE_COLORS = [(199, 54, 37)]
BACK_GROUND_COLORS = [(54, 45, 62)]
POKEMON_KO_COLORS = [(91, 33, 31)]
POKEMON_KO_SELECTED_COLORS = [(145, 11, 66)]
POKEMON_ALIVE_COLORS = [(11, 35, 59)]
MONEY_COLORS = [(232, 232, 168), (160, 160, 96)]

# Allowed color difference
COLOR_TOLERANCE = 10

# Number of sample points to check in a region (grid)
SAMPLE_GRID_SIZE = 3  # Will sample 3x3 grid = 9 points per region

# =========================
# STATE
# =========================

isRunning = False
programRunning = True

pyautogui.FAILSAFE = True


# =========================
# HELPERS
# =========================

def color_close(c1, c2, tolerance):
    """
    Compare two RGB colors with tolerance.
    """
    return all(abs(a - b) <= tolerance for a, b in zip(c1, c2))


def get_region_pixels(x, y, width, height, grid_size=3):
    """
    Sample multiple pixels from a region in a grid pattern.
    Returns a list of (x, y, color) tuples for sampled pixels.
    grid_size: number of sample points per dimension (3 = 3x3 grid)
    """
    screenshot = pyautogui.screenshot()
    pixels = []
    
    # Calculate step size between samples
    x_step = width / (grid_size + 1) if grid_size > 0 else width / 2
    y_step = height / (grid_size + 1) if grid_size > 0 else height / 2
    
    # Sample pixels in a grid
    for i in range(1, grid_size + 1):
        for j in range(1, grid_size + 1):
            sample_x = int(x + x_step * i)
            sample_y = int(y + y_step * j)
            color = screenshot.getpixel((sample_x, sample_y))
            pixels.append((sample_x, sample_y, color))
    
    return pixels


def region_matches_any_color(x, y, width, height, target_colors, grid_size=3):
    """
    Check if a region contains pixels matching any of the target colors.
    Returns True if at least one sampled pixel matches at least one target color.
    """
    sampled_pixels = get_region_pixels(x, y, width, height, grid_size)
    
    for _, _, pixel_color in sampled_pixels:
        for target_color in target_colors:
            if color_close(pixel_color, target_color, COLOR_TOLERANCE):
                print(f"  Region ({x},{y}): Found matching color {pixel_color} ≈ {target_color}")
                return True
    
    # Debug: show what we found
    if sampled_pixels:
        print(f"  Region ({x},{y}): Sampled colors - {[p[2] for p in sampled_pixels]}")
    
    return False


def detect_state():
    """
    Detect game state using region-based color matching.
    """
    print("\n--- State Detection ---")
    
    # Check if we're in menu
    if region_matches_any_color(*REGION_BOX_MENU, MENU_BACKGROUND_COLORS, SAMPLE_GRID_SIZE):
        print("Detected: MENU state")
        
        # Check pokemon states in menu
        pokemon_1_ko = region_matches_any_color(
            *REGION_POKEMON_1_MENU, 
            POKEMON_KO_COLORS + POKEMON_KO_SELECTED_COLORS, 
            SAMPLE_GRID_SIZE
        )
        pokemon_2_ko = region_matches_any_color(
            *REGION_POKEMON_2_MENU,
            POKEMON_KO_COLORS + POKEMON_KO_SELECTED_COLORS,
            SAMPLE_GRID_SIZE
        )
        
        if pokemon_1_ko or pokemon_2_ko:
            print("Detected: MENU KO state")
            return GameState.MENU_KO
        
        # Check if battle money indicator is visible (in menu)
        if region_matches_any_color(*REGION_MONEY, MONEY_COLORS, SAMPLE_GRID_SIZE):
            print("Detected: BATTLE state (from menu view)")
            return GameState.BATTLE
        
        return GameState.MENU

    # Check if we're in battle
    if region_matches_any_color(*REGION_BOX_BATTLE, BOX_OUTLINE_COLORS + BACK_GROUND_COLORS, SAMPLE_GRID_SIZE):
        print("Detected: BATTLE state")
        return GameState.BATTLE

    print("Detected: UNKNOWN state")
    return GameState.UNKNOWN

# =========================
# ACTIONS
# =========================

def handle_menu():
    print("[MENU] Pressing X")
    pyautogui.press("x")

def handle_battle():
    print("[BATTLE] Pressing Enter")
    pyautogui.press("enter")

def handle_menue_ko():
    print("[MENU KO] Pressing DOWN")
    pyautogui.press("s")
    time.sleep(0.2)
    print("[MENU KO] Pressing Enter")
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("enter")

# =========================
# KEYBOARD CONTROLS
# =========================

def on_press(key):
    global isRunning
    global programRunning

    try:

        # START / RESUME
        if key == keyboard.Key.f8:
            if not isRunning:
                isRunning = True
                print("Bot started")

        # PAUSE
        elif key == keyboard.Key.esc:
            if isRunning:
                isRunning = False
                print("Bot paused")

        # FULL QUIT
        elif key == keyboard.Key.f9:
            print("Program terminated")
            programRunning = False
            return False

    except Exception as e:
        print(e)


listener = keyboard.Listener(on_press=on_press)
listener.start()

print("===================================")
print("F8  -> Start / Resume bot")
print("ESC -> Pause bot")
print("F9  -> Quit program")
print("===================================")

# =========================
# MAIN LOOP
# =========================

while programRunning:

    if not isRunning:
        time.sleep(0.1)
        continue

    try:

        state = detect_state()

        print(f"Detected state: {state}")

        if state == GameState.MENU:
            handle_menu()

        elif state == GameState.BATTLE:
            handle_battle()

        elif state == GameState.MENU_KO:
            handle_menue_ko()

        else:
            print("[UNKNOWN] Doing nothing")

    except pyautogui.FailSafeException:
        print("Failsafe triggered (mouse moved to top-left)")
        isRunning = False

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(SCAN_INTERVAL)

print("Program closed.")
