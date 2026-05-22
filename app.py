import json
import os
from pathlib import Path
from flask import Flask, jsonify, render_template, request

from fare_calculator import calculate_fare, resolve_station

app = Flask(__name__)

STATIONS_FILE = Path(__file__).parent / 'stations.json'
with STATIONS_FILE.open(encoding='utf-8') as f:
    STATIONS = json.load(f)['stations']

def _stations_by_line():
    grouped = {}
    for s in STATIONS:
        grouped.setdefault(s['line'], []).append(s)
    return grouped

@app.route('/')
def index():
    return render_template('index.html', stations_by_line=_stations_by_line())

@app.route('/api/stations')
def list_stations():
    return jsonify({'count': len(STATIONS), 'stations': STATIONS})

@app.route('/api/fare')
def fare():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify({'error': 'Both "source" and "destination" query parameters are required'}), 400

    canonical_source = resolve_station(source)
    if canonical_source is None:
        return jsonify({'error': f"Station '{source}' not found"}), 400

    canonical_destination = resolve_station(destination)
    if canonical_destination is None:
        return jsonify({'error': f"Station '{destination}' not found"}), 400

    if canonical_source == canonical_destination:
        return jsonify({'error': 'Source and destination cannot be the same'}), 400

    result = calculate_fare(canonical_source, canonical_destination)
    return jsonify({
        'source': canonical_source,
        'destination': canonical_destination,
        'distance_km': result['distance_km'],
        'fare': result['fare'],
        'interchanges': result['interchanges'],
        'is_same_line': len(result['interchanges']) == 0,
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
