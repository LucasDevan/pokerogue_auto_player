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
from gameState import GameState
from pokemon import Pokemon
from color import Color

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
REGION_POKEMON_1_MENU = (564, 429, 30, 30)
REGION_POKEMON_2_MENU = (600, 900, 30, 30)
REGION_MONEY = (656, 976, 30, 30)

# RGB reference values - using Color class instances
MENU_BACKGROUND_COLORS = [Color(16, 24, 32)]
BOX_OUTLINE_COLORS = [Color(199, 54, 37)]
BACK_GROUND_COLORS = [Color(54, 45, 62)]
POKEMON_KO_COLORS = [Color(91, 33, 31)]
POKEMON_KO_SELECTED_COLORS = [Color(145, 11, 66)]
POKEMON_ALIVE_COLORS = [Color(11, 35, 59)]
MONEY_COLORS = [Color(232, 232, 168), Color(160, 160, 96)]


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
            if pixel_color.are_close(target_color):
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
