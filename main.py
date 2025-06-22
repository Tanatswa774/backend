import time
import threading
import bot_state
from adb_utils import take_screenshot, tap, swipe
from scanner import find_template

TEMPLATE_PATH = "templates/gem.png"
GATHER_PATH = "templates/gather.png"
MAX_MARCHES = 5

def swipe_map():
    directions = [
        (800, 500, 300, 500),   # left
        (300, 500, 800, 500),   # right
        (500, 800, 500, 300),   # up
        (500, 300, 500, 800),   # down
    ]
    for d in directions:
        swipe(*d)
        time.sleep(2)

def reset_march_after_delay(delay: int = 180):
    def reset():
        time.sleep(delay)
        bot_state.active_marches = max(0, bot_state.active_marches - 1)
        print(f"✅ March returned. Active marches: {bot_state.active_marches}")
    threading.Thread(target=reset, daemon=True).start()

def gather_gems():
    if bot_state.active_marches >= MAX_MARCHES:
        print("⛔ All marches are currently busy.")
        return

    take_screenshot()
    matches = find_template("screenshot.png", TEMPLATE_PATH)

    for (x, y) in matches:
        print(f"💎 Found gem at ({x},{y})")
        tap(x + 20, y + 20)
        time.sleep(2)

        take_screenshot()
        gather_matches = find_template("screenshot.png", GATHER_PATH, threshold=0.7)

        if gather_matches:
            gx, gy = gather_matches[0]
            print(f"🎯 Gather button at ({gx},{gy}) — dispatching march")
            tap(gx + 10, gy + 10)
            bot_state.active_marches += 1
            print(f"🚶‍♂️ Active marches: {bot_state.active_marches}")
            reset_march_after_delay()
            time.sleep(3)
        else:
            print("⚠️ Gather button not found after tapping gem.")
        break  # One gem per run

def run_bot_loop():
    bot_state.bot_running = True
    print("🚀 Bot started.")
    while bot_state.bot_running:
        swipe_map()
        gather_gems()
        time.sleep(10)
    print("🛑 Bot stopped.")
