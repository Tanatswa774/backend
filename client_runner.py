import time
import requests
import bot_state
from main import run_bot_loop

# Replace this with your actual Render backend URL
API_BASE = "https://rok-flask-backend.onrender.com"

def check_and_run_bot():
    print("📡 Starting bot poller...")
    while True:
        try:
            response = requests.get(f"{API_BASE}/status")
            if response.status_code == 200:
                status = response.json()
                is_online = status.get("running", False)

                if is_online and not bot_state.bot_running:
                    print("🟢 Bot turned ON remotely. Starting bot loop...")
                    bot_state.bot_running = True
                    run_bot_loop()
                elif not is_online and bot_state.bot_running:
                    print("🔴 Bot turned OFF remotely. Stopping bot loop...")
                    bot_state.bot_running = False
            else:
                print(f"⚠️ Failed to get status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error checking server: {e}")

        time.sleep(5)  # check every 5 seconds

if __name__ == "__main__":
    check_and_run_bot()
