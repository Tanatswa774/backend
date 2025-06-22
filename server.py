from flask import Flask, jsonify, send_file
from flask_cors import CORS
import threading
import os
from typing import Optional

import bot_state
from main import run_bot_loop

app = Flask(__name__)
CORS(app)

bot_thread: Optional[threading.Thread] = None
bot_lock = threading.Lock()
stop_signal = False

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_thread
    with bot_lock:
        if bot_state.bot_running:
            return jsonify({"message": "Bot already running"}), 409
        bot_state.bot_running = True
        bot_thread = threading.Thread(target=run_bot_loop, daemon=True)
        bot_thread.start()
        return jsonify({"message": "Bot started"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    with bot_lock:
        if not bot_state.bot_running:
            return jsonify({"message": "Bot is not running"}), 409
        bot_state.bot_running = False
        return jsonify({"message": "Stopping bot"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "running": bot_state.bot_running,
        "active_marches": bot_state.active_marches
    })

@app.route('/screenshot', methods=['GET'])
def screenshot():
    screenshot_path = os.path.abspath("screenshot.png")
    if not os.path.exists(screenshot_path):
        return jsonify({"error": "No screenshot available"}), 404
    return send_file(screenshot_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
