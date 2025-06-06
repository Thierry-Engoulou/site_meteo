from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PREVISIONS_PATH = os.path.join(DATA_DIR, "previsions.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/previsions/<ville>')
def previsions(ville):
    with open(PREVISIONS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data.get(ville, []))

if __name__ == '__main__':
    app.run(debug=True)