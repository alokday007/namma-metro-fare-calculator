# 🚇 Namma Metro Fare Calculator

A Flask-based fare calculator for Bengaluru's Namma Metro (BMRCL). Enter any two stations across the Purple, Green, or Yellow lines and get the estimated fare based on BMRCL's distance-slab pricing.

## Features

- 85 operational stations across **Purple**, **Green**, and **Yellow** lines (as of May 2026)
- Distance-based fare calculation using current BMRCL slabs (₹10–₹90)
- Cross-line journeys handled automatically:
  - **Purple ↔ Green** via Majestic (Nadaprabhu Kempegowda Station)
  - **Green ↔ Yellow** via RV Road (Rashtreeya Vidyalaya Road)
  - **Purple ↔ Yellow** via both interchanges (double transfer)
- JSON API endpoint to list all stations
- Standalone fare module — usable without Flask for scripting/testing

## Tech Stack

- **Python 3** — core language
- **Flask** — web framework
- **JSON** — station data store

## Getting Started

```bash
# 1. Clone
git clone https://github.com/alokday007/namma-metro-fare-calculator.git
cd namma-metro-fare-calculator

# 2. Create and activate a virtual environment
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install flask

# 4. Run the Flask app
python app.py
```

Then open `http://127.0.0.1:5000/api/stations` to verify the station list loads.

To run the fare logic tests:

```bash
python test_fare.py
```

## Project Structure

```
namma-metro-fare-calculator/
├── app.py                 # Flask app and routes
├── fare_calculator.py     # Distance + fare calculation logic
├── test_fare.py           # Sample journey tests
├── stations.json          # 85 operational stations (Purple/Green/Yellow)
├── README.md
├── .gitignore
└── venv/                  # Virtual environment (gitignored)
```

## Sample Test Results

Running `python test_fare.py`:

```
PASS  Short same-line (Purple, 2 hops)
      Indiranagar  ->  Halasuru
      distance=2.42 km   fare=Rs.20   expected~Rs.20   interchanges=[]

PASS  Medium same-line (Green, Yeshwanthpur -> Majestic, ~10 km)
      Yeshwanthpur  ->  Nadaprabhu Kempegowda Station, Majestic
      distance=7.56 km   fare=Rs.40   expected~Rs.50   interchanges=[]

PASS  Full Purple end-to-end (cap)
      Whitefield (Kadugodi)  ->  Challaghatta
      distance=43.49 km  fare=Rs.90   expected~Rs.90   interchanges=[]

PASS  Purple <-> Green via Majestic (Indiranagar -> Banashankari)
      Indiranagar  ->  Banashankari
      distance=16.04 km  fare=Rs.70   expected~Rs.70   interchanges=['Nadaprabhu Kempegowda Station, Majestic']

PASS  Green <-> Yellow via RV Road (Jayanagar -> Electronic City)
      Jayanagar  ->  Electronic City
      distance=16.25 km  fare=Rs.70   expected~Rs.60   interchanges=['Rashtreeya Vidyalaya Road']

PASS  Purple <-> Yellow double interchange (Whitefield -> Bommasandra)
      Whitefield (Kadugodi)  ->  Bommasandra
      distance=52.40 km  fare=Rs.90   expected~Rs.90   interchanges=['Nadaprabhu Kempegowda Station, Majestic', 'Rashtreeya Vidyalaya Road']

6/6 passed (tolerance +/- Rs.10)
```

## Screenshots

_Coming soon — UI is under development._

<!--
![Home page](docs/screenshots/home.png)
![Fare result](docs/screenshots/fare-result.png)
-->

## Credits

- **[BMRCL](https://bmrc.co.in)** — official fare slabs and route data
- **[Flask](https://flask.palletsprojects.com/)** — Python web framework
- Station data cross-referenced with Wikipedia line articles (Purple, Green, Yellow)

---

_Built as a learning project. Fares are estimates based on average inter-station distances; refer to the official BMRCL fare chart for exact pricing._
