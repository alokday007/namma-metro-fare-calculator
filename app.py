import json
from pathlib import Path
from flask import Flask, jsonify, request

from fare_calculator import calculate_fare, resolve_station

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
    app.run(debug=True)
