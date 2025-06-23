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

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Server is running"})

@app.route('/start', methods=['POST'])  # ✅ POST explicitly declared here
def start_bot():
    global bot_thread
    with bot_lock:
        if bot_state.bot_running:
            return jsonify({"message": "Bot already running"}), 409
        bot_state.bot_running = True
        bot_thread = threading.Thread(target=run_bot_loop, daemon=True)
        bot_thread.start()
        return jsonify({"message": "Bot started"})

@app.route('/stop', methods=['POST'])  # ✅ POST explicitly declared here
def stop_bot():
    with bot_lock:
        if not bot_state.bot_running:
            return jsonify({"message": "Bot is not running"}), 409
        bot_state.bot_running = False
        return jsonify({"message": "Bot stopping"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "running": bot_state.bot_running,
        "active_marches": bot_state.active_marches
    })

@app.route('/screenshot', methods=['GET'])
def screenshot():
    path = os.path.abspath("screenshot.png")
    if not os.path.exists(path):
        return jsonify({"error": "No screenshot found"}), 404
    return send_file(path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
