
import time
import threading
import bot_state
from adb_utils import take_screenshot, tap, swipe
from scanner import find_template

GEM_TEMPLATES = [
    "templates/gem1.png",
    "templates/gem2.png",
    "templates/gem3.png",
    "templates/gem4.png"
]
GATHER_PATH = "templates/gather.png"
MAX_MARCHES = 5

def swipe_map():
    directions = [
        (800, 500, 300, 500),
        (300, 500, 800, 500),
        (500, 800, 500, 300),
        (500, 300, 500, 800)
    ]
    for d in directions:
        swipe(*d)
        time.sleep(2)

def reset_march_after_delay(delay: int = 180):
    def reset():
        time.sleep(delay)
        bot_state.active_marches = max(0, bot_state.active_marches - 1)
        print(f"March returned. Active marches: {bot_state.active_marches}")
    threading.Thread(target=reset, daemon=True).start()

def gather_gems():
    if bot_state.active_marches >= MAX_MARCHES:
        print("All marches busy.")
        return

    take_screenshot()
    for template_path in GEM_TEMPLATES:
        matches = find_template("screenshot.png", template_path, threshold=0.75)
        if matches:
            for (x, y) in matches:
                print(f"Gem found at ({x}, {y}) with {template_path}")
                tap(x + 20, y + 20)
                time.sleep(2)

                take_screenshot()
                gather_matches = find_template("screenshot.png", GATHER_PATH, threshold=0.7)

                if gather_matches:
                    gx, gy = gather_matches[0]
                    tap(gx + 10, gy + 10)
                    bot_state.active_marches += 1
                    print(f"Gathering. Active marches: {bot_state.active_marches}")
                    reset_march_after_delay()
                    time.sleep(3)
                else:
                    print("Gather button not found.")
                return  # Stop after finding 1 gem
    print("No gems found.")
