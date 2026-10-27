# PokeRogue Auto Player

A small Python experiment that attempts to play parts of the browser game
PokeRogue by inspecting screen pixels and sending keyboard input. This project
was created as a programming exercise and demonstration of my abilities, not
as a finished or generally usable product.

## Status and expectations

**This project is very much a work in progress.** It is experimental, has not
been made portable, and is unlikely to work on most computers without
substantial adjustments. It is also nowhere near reliably playing PokeRogue
at an acceptable level of skill. Expect incorrect state detection, poor
decisions, and situations that need manual intervention.

The project currently uses fixed screen coordinates and example pixel colors.
These assumptions depend on the display, browser, game layout, and scaling, so
the program may not recognize your screen correctly. Its gameplay logic is
deliberately simple and only handles a limited set of game screens.

## What it does

- Captures screenshots and samples selected screen regions.
- Tries to identify menus, battles, shops, move learning, and some other game
  states by matching pixel colors.
- Sends basic keyboard input to navigate menus and choose moves.
- Lets you start, pause, or quit the automation with global keyboard shortcuts.

This is not a game client, a general-purpose computer-vision system, or a
competitive player. PokeRogue is not included; open it separately before
running the script.

## Requirements

- Python installed and available from your terminal.
- The Python packages `pyautogui`, `pynput`, and `Pillow`.
- PokeRogue open on screen in a layout you have configured the script to
  recognize.

Install the dependencies from the repository directory:

```bash
python -m pip install pyautogui pynput pillow
```

Depending on your system, `pynput` may require accessibility or input-control
permissions. `pyautogui` also relies on screen-capture support provided by your
operating system.

## Running

From the repository directory, run:

```bash
python main.py
```

The bot starts paused. Use these keys:

| Key | Action |
| --- | --- |
| `F8` | Start or resume the bot |
| `Esc` | Pause the bot |
| `F9` | Quit the program |

The script enables PyAutoGUI's fail-safe: moving the mouse to the top-left
corner of the screen triggers a pause. Keep the game visible and be ready to
pause or quit if the automation behaves unexpectedly.

## Configuration and limitations

Before expecting the bot to recognize your game, inspect the screen regions,
reference colors, and move-slot coordinates near the top of
[`main.py`](./main.py). They are example values, not automatically calibrated
settings. You may need to adjust them for your display resolution, browser
zoom, window position, and game interface.

The current implementation relies on coarse color matching and fixed
coordinates. It does not reliably understand game context, make strategic
decisions, or handle every game state. Treat it as a prototype to explore and
adapt, not as dependable automation.

## Distribution and modifications

You are welcome to distribute and modify this project. There is no separate
license file in the repository at this time, so no standard open-source
license terms have been specified.

## Acknowledgements

This project is an unofficial fan-made experiment and is not affiliated with
the PokeRogue project. PokeRogue is the work being explored here; visit the
[PokeRogue wiki](https://wiki.pokerogue.net/start) to learn about the game.