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

import random
import time
import pyautogui
from pynput import keyboard
from gameState import GameState
from pokemon import Pokemon
from color import Color
from pixel import Pixel

# =========================
# CONFIG
# =========================

SCAN_INTERVAL = 0.5

# Example coordinates/colors
# You MUST adapt these to your setup
# Format: (x, y, width, height) - defines a region to sample from

# Regions to check (top-left corner + size)
REGION_BOX_BATTLE = (2417, 1224, 20, 20)
REGION_BOX_MENU = (140, 120, 20, 20)
ENNEMY_POKEMON_1_STATUS_WINDOW = (500,280,50,10)
ENNEMY_POKEMON_2_STATUS_WINDOW = (500,500,50,10)
REGION_POKEMON_1_MENU = (564, 429, 15, 15)
REGION_POKEMON_2_MENU = (600, 900, 15, 15)
REGION_MONEY = (500, 960, 25, 15)
REGION_PP_LEFT = (2400,1233,20,10)

# RGB reference values - using Color class instances
MENU_BACKGROUND_COLORS = [Color(16, 24, 32)]
BOX_OUTLINE_COLORS = [Color(199, 54, 37)]
BACK_GROUND_COLORS = [Color(54, 45, 62)]
POKEMON_KO_COLORS = [Color(91, 33, 31)]
POKEMON_KO_SELECTED_COLORS = [Color(145, 11, 66)]
POKEMON_ALIVE_COLORS = [Color(11, 35, 59)]
MONEY_COLORS = [Color(232, 232, 168), Color(160, 160, 96)]

SUPER_EFFECTIVE_COLORS = [Color(75, 180, 0),Color(72, 155, 5)]
EFFECTIVE_COLORS = [Color(248, 248, 248)]
NOT_EFFECTIVE_COLORS = [Color(254, 142, 0)]
INEFFECTIVE_COLORS = [Color(180, 180, 0)]

def getEffectivennesLevelColor(level : int) -> list:
    if (level == 1):
        return SUPER_EFFECTIVE_COLORS
    if (level==2):
        return EFFECTIVE_COLORS
    if (level == 3):
        return NOT_EFFECTIVE_COLORS
    if (level==4):
            return INEFFECTIVE_COLORS
    return EFFECTIVE_COLORS

def getEffectivennesLevelColorName(level : int) -> str:
    if (level == 1):
        return "SUPER_EFFECTIVE_COLORS"
    if (level==2):
        return "EFFECTIVE_COLORS"
    if (level == 3):
        return "NOT_EFFECTIVE_COLORS"
    if (level==4):
            return "INEFFECTIVE_COLORS"
    return "error"

MOVE_1_SLOT = (160,1190,20,20)
MOVE_2_SLOT = (160,1320,20,20)
MOVE_3_SLOT = (1070,1190,20,20)
MOVE_4_SLOT = (1070,1320,20,20)

# =========================
# STATE
# =========================

AUTOPLAYER_IS_PLAYING = False
PROGRAM_IS_RUNNING = True

current_selected_move_slot_pk_1 = 1
current_selected_move_slot_pk_2 = 1

pyautogui.FAILSAFE = True

# =========================
# HELPERS
# =========================
def get_region_pixels(x, y, width, height):
    """
    Returns a list of Pixel objects.
    """
    screenshot = pyautogui.screenshot()
    pixels : list  = []
    color : Color
    previousColor : Color = Color(-50,-50,-50)
    # Sample pixels in a grid
    for i in range(x - round(width/2), x + round(width/2)):
        for j in range(y - round(height/2), y + round(height/2)):
            rgb_tuple = screenshot.getpixel((i, j))
            color = Color(*rgb_tuple)
            #print("i ",i," j ",j," color: ",color.get_color())
            if(not(color.are_close(previousColor,0))):
                pixels.append(Pixel(i, j, color))
                previousColor = color
    
    return pixels

def region_matches_a_color(x  : float, y  : float, width  : float, height : float, target_colors: Color):
    return region_matches_any_color(x, y, width, height, [target_colors])

def region_matches_any_color(x :float, y : float, width : float, height : float , target_colors: list):
    """
    Check if a region contains pixels matching any of the target colors.
    Returns True if at least one sampled pixel matches at least one target color.
    """
    screenshot = pyautogui.screenshot()

    for i in range(x - round(width/2), x + round(width/2)):
        for j in range(y - round(height/2), y + round(height/2)):
            rgb_tuple = screenshot.getpixel((i, j))
            color = Color(*rgb_tuple)
            #print("i ",i," j ",j," color: ",color.get_color())
            for c in range(len(target_colors)):
                if(color.are_close(target_colors[c])):
                    print(f"  Region ({x},{y}): Found matching color {color.get_color()} ≈ {target_colors[c].get_color()}")
                    return True
    

    return False


def detect_state():
    """
    Detect game state using region-based color matching.
    """
    print("\n--- State Detection ---")
    
    # Check if we're in menu
    if region_matches_any_color(*REGION_BOX_MENU, MENU_BACKGROUND_COLORS):
        print("Detected: MENU state")
        
        # Check pokemon states in menu
        pokemon_1_ko : bool = region_matches_any_color(*REGION_POKEMON_1_MENU, POKEMON_KO_COLORS + POKEMON_KO_SELECTED_COLORS)
        pokemon_2_ko : bool  = region_matches_any_color(*REGION_POKEMON_2_MENU,POKEMON_KO_COLORS + POKEMON_KO_SELECTED_COLORS)
        
        if pokemon_1_ko or pokemon_2_ko:
            print("Detected: MENU KO state")
            return GameState.MENU_KO
        
        # Check if battle money indicator is visible (in menu)
        if region_matches_any_color(*REGION_MONEY, MONEY_COLORS):
            print("Detected: BATTLE state (from menu view)")
            return GameState.BATTLE
        
        return GameState.MENU

    # Check if we are in shop indicated by the money region
    if region_matches_any_color(*REGION_MONEY, MONEY_COLORS):
        print("Detected: SHOP state")
        return GameState.SHOP   

    # Check if we're in battle
    if region_matches_any_color(*REGION_BOX_BATTLE, BOX_OUTLINE_COLORS + BACK_GROUND_COLORS):
        if region_matches_any_color(*ENNEMY_POKEMON_1_STATUS_WINDOW,BACK_GROUND_COLORS) and region_matches_any_color(*ENNEMY_POKEMON_2_STATUS_WINDOW,BACK_GROUND_COLORS):
            print("Detected: DOUBLE BATTLE state")
            return GameState.DOUBLE_BATTLE
        print("Detected: BATTLE state")
        return GameState.BATTLE

    print("Detected: UNKNOWN state")
    return GameState.UNKNOWN

def detect_best_move() -> int:
    counter : int = 1
    colors : list
    while(counter <= 4):
        print("Checking for color ",getEffectivennesLevelColorName(counter))
        colors = getEffectivennesLevelColor(counter)
        if region_matches_any_color(*MOVE_1_SLOT,colors):
            return 1
        if region_matches_any_color(*MOVE_2_SLOT,colors):
            return 2
        if region_matches_any_color(*MOVE_3_SLOT,colors):
            return 3
        if region_matches_any_color(*MOVE_4_SLOT,colors):
            return 4
        counter += 1
    return 0

# =========================
# ACTIONS
# =========================
def in_move_select_to_move_slot(move_number : int, startFrom = current_selected_move_slot_pk_1):
    if(move_number <= 0 or move_number > 4):
        print(f"Invalid move number: {move_number}. Must be between 1 and 4.")
        return
    if(startFrom <= 0 or move_number > 4):
        startFrom = 1

    if(move_number != startFrom):
        print("Going from ",startFrom," to ",move_number)

        if((startFrom == 1 and move_number == 2) or (startFrom == 3 and move_number == 4)):
            print("going down")
            pyautogui.press("s")
        elif((startFrom == 1 and move_number == 3) or (startFrom == 2 and move_number == 4)):
            print("going right")
            pyautogui.press("d")
        elif((startFrom == 3 and move_number == 1) or (startFrom == 4 and move_number == 2)):
            print("going left")
            pyautogui.press("a")
        elif((startFrom == 2 and move_number == 1) or (startFrom == 4 and move_number == 3)):
            print("going up")
            pyautogui.press("w")
        else:
            print("Going by setps")
            if(startFrom == 1):
                in_move_select_to_move_slot(2,startFrom)
                time.sleep(0.4)
                in_move_select_to_move_slot(move_number,2)
            elif(startFrom == 2):
                in_move_select_to_move_slot(1,startFrom)
                in_move_select_to_move_slot(move_number,1)
            elif(startFrom == 3):
                in_move_select_to_move_slot(1,startFrom)
                in_move_select_to_move_slot(move_number,1)
            elif(startFrom == 4):
                in_move_select_to_move_slot(2,startFrom)
                in_move_select_to_move_slot(move_number,2)
    current_selected_move_slot_pk_1 = move_number
    time.sleep(0.4)

def handle_menu():
    print("[MENU] Pressing X")
    pyautogui.press("x")

def handle_battle(handling_pokemon_number = 1):
    pyautogui.press("enter")
    selected_move = detect_best_move()
    print("[BATTLE] choosing move",selected_move)
    if(handling_pokemon_number == 1):
        in_move_select_to_move_slot(selected_move,current_selected_move_slot_pk_1)
    else:
        in_move_select_to_move_slot(selected_move,current_selected_move_slot_pk_2)
    pyautogui.press("enter")
    time.sleep(0.1)

def handle_double_battle():
    handle_battle(1)#pk 1
    pyautogui.press("enter")
    time.sleep(0.4)
    handle_battle(2)#pk 2
    pyautogui.press("enter")

def handle_menu_ko():
    print("[MENU KO] Pressing DOWN")
    pyautogui.press("s")
    time.sleep(0.1)
    print("[MENU KO] Pressing Enter")
    pyautogui.press("enter")
    time.sleep(0.1)
    pyautogui.press("enter")


def handle_shop():
    print("[SHOP] Pressing Enter")
    pyautogui.press("x")
    time.sleep(0.4)
    pyautogui.press("enter")


# =========================
# KEYBOARD CONTROLS
# =========================

def on_press(key):
    global AUTOPLAYER_IS_PLAYING
    global PROGRAM_IS_RUNNING

    try:

        # START / RESUME
        if key == keyboard.Key.f8:
            if not AUTOPLAYER_IS_PLAYING:
                AUTOPLAYER_IS_PLAYING = True
                print("Bot started")

        # PAUSE
        elif key == keyboard.Key.esc:
            if AUTOPLAYER_IS_PLAYING:
                AUTOPLAYER_IS_PLAYING = False
                print("Bot paused")

        # FULL QUIT
        elif key == keyboard.Key.f9:
            print("Program terminated")
            PROGRAM_IS_RUNNING = False
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

while PROGRAM_IS_RUNNING:

    if not AUTOPLAYER_IS_PLAYING:
        time.sleep(0.1)
        continue

    try:
        state = detect_state()

        print(f"Detected state: {state}")

        if state == GameState.MENU:
            handle_menu()

        elif state == GameState.BATTLE:
            handle_battle()

        elif state == GameState.DOUBLE_BATTLE:
            handle_double_battle()

        elif state == GameState.MENU_KO:
            handle_menu_ko()

        elif state == GameState.SHOP:
            handle_shop()

        else:
            print("[UNKNOWN] Doing nothing")

    except pyautogui.FailSafeException:
        print("Failsafe triggered (mouse moved to top-left)")
        AUTOPLAYER_IS_PLAYING = False

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(SCAN_INTERVAL)

print("Program closed.")
