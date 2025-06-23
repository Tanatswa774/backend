from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Server is running"})

@app.route('/start', methods=['POST'])
def start_bot():
    return jsonify({"message": "Start endpoint working!"})

if __name__ == '__main__':
    app.run(debug=True)
