"""Namma Metro fare calculator.

Distance model (v1): average inter-station distance per line, computed from
published line length / (stations - 1). Real chainage would be more accurate
but isn't in stations.json yet.

Fare slabs from BMRCL chart in effect May 2026 (Feb 2026 hike on hold).
"""

import json
from pathlib import Path

STATIONS_FILE = Path(__file__).parent / 'stations.json'

LINE_LENGTHS_KM = {
    'Purple': 43.49,
    'Green': 33.46,
    'Yellow': 19.15,
}

FARE_SLABS = [
    (2, 10),
    (4, 20),
    (6, 30),
    (8, 40),
    (10, 50),
    (15, 60),
    (20, 70),
    (25, 80),
]
MAX_FARE = 90

INTERCHANGES = {
    frozenset(('Purple', 'Green')): 'Nadaprabhu Kempegowda Station, Majestic',
    frozenset(('Green', 'Yellow')): 'Rashtreeya Vidyalaya Road',
}


def _load_stations():
    with STATIONS_FILE.open(encoding='utf-8') as f:
        return json.load(f)['stations']


_STATIONS = _load_stations()

_BY_LINE = {}
for s in _STATIONS:
    _BY_LINE.setdefault(s['line'], {})[s['name']] = s

_AVG_HOP_KM = {
    line: LINE_LENGTHS_KM[line] / (len(stations) - 1)
    for line, stations in _BY_LINE.items()
}


_CANONICAL_BY_LOWER = {s['name'].lower(): s['name'] for s in _STATIONS}


def resolve_station(name):
    """Return the canonical station name for a case-insensitive input, or None."""
    if name is None:
        return None
    return _CANONICAL_BY_LOWER.get(name.strip().lower())


def _lines_for(name):
    return [line for line, stns in _BY_LINE.items() if name in stns]


def _segment(line, from_name, to_name):
    a = _BY_LINE[line][from_name]['order']
    b = _BY_LINE[line][to_name]['order']
    hops = abs(a - b)
    km = hops * _AVG_HOP_KM[line]
    return {'line': line, 'from': from_name, 'to': to_name, 'hops': hops, 'km': round(km, 2)}


def _fare_for_km(km):
    for limit, fare in FARE_SLABS:
        if km <= limit:
            return fare
    return MAX_FARE


def calculate_fare(from_station, to_station):
    """Return fare details for a journey between two station names.

    Picks the cheapest line option if a station name exists on multiple lines.
    """
    from_lines = _lines_for(from_station)
    to_lines = _lines_for(to_station)
    if not from_lines:
        raise ValueError(f"Unknown station: {from_station}")
    if not to_lines:
        raise ValueError(f"Unknown station: {to_station}")

    best = None
    for fl in from_lines:
        for tl in to_lines:
            result = _route(from_station, fl, to_station, tl)
            if best is None or result['distance_km'] < best['distance_km']:
                best = result
    return best


def _route(from_station, from_line, to_station, to_line):
    legs = []
    interchanges = []

    if from_line == to_line:
        legs.append(_segment(from_line, from_station, to_station))
    else:
        key = frozenset((from_line, to_line))
        if key in INTERCHANGES:
            ix = INTERCHANGES[key]
            legs.append(_segment(from_line, from_station, ix))
            legs.append(_segment(to_line, ix, to_station))
            interchanges.append(ix)
        else:
            # Purple <-> Yellow: must transit Green via Majestic then RV Road
            majestic = INTERCHANGES[frozenset(('Purple', 'Green'))]
            rv_road = INTERCHANGES[frozenset(('Green', 'Yellow'))]
            if from_line == 'Purple' and to_line == 'Yellow':
                legs.append(_segment('Purple', from_station, majestic))
                legs.append(_segment('Green', majestic, rv_road))
                legs.append(_segment('Yellow', rv_road, to_station))
            else:  # Yellow -> Purple
                legs.append(_segment('Yellow', from_station, rv_road))
                legs.append(_segment('Green', rv_road, majestic))
                legs.append(_segment('Purple', majestic, to_station))
            interchanges.extend([majestic, rv_road])

    total_km = round(sum(leg['km'] for leg in legs), 2)
    return {
        'from': from_station,
        'to': to_station,
        'distance_km': total_km,
        'fare': _fare_for_km(total_km),
        'interchanges': interchanges,
        'route': legs,
    }


if __name__ == '__main__':
    import pprint
    pprint.pp(calculate_fare('Indiranagar', 'Banashankari'))
