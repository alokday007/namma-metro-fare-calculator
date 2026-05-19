import json
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)

STATIONS_FILE = Path(__file__).parent / 'stations.json'
with STATIONS_FILE.open(encoding='utf-8') as f:
    STATIONS = json.load(f)['stations']

@app.route('/')
def hello():
    return '<h1>Namma Metro Fare Calculator - Coming Soon!</h1>'

@app.route('/api/stations')
def list_stations():
    return jsonify({'count': len(STATIONS), 'stations': STATIONS})

if __name__ == '__main__':
    app.run(debug=True)
