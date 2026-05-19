"""Sanity tests for fare_calculator. Tolerance: +/- one slab (Rs 10)."""

from fare_calculator import calculate_fare

TOLERANCE = 10

CASES = [
    # (description, from, to, expected_fare)
    ("Short same-line (Purple, 2 hops)",
     "Indiranagar", "Halasuru", 20),

    ("Medium same-line (Green, ~10 km)",
     "Yeshwanthpur", "Majestic_GREEN", 50),  # placeholder, fixed below

    ("Full Purple end-to-end (cap)",
     "Whitefield (Kadugodi)", "Challaghatta", 90),

    ("Purple <-> Green via Majestic (Indiranagar -> Banashankari)",
     "Indiranagar", "Banashankari", 70),

    ("Green <-> Yellow via RV Road (Jayanagar -> Electronic City)",
     "Jayanagar", "Electronic City", 60),

    ("Purple <-> Yellow double interchange (Whitefield -> Bommasandra)",
     "Whitefield (Kadugodi)", "Bommasandra", 90),
]

# Fix the placeholder: use the Green-line Majestic station name
CASES[1] = (
    "Medium same-line (Green, Yeshwanthpur -> Majestic, ~10 km)",
    "Yeshwanthpur",
    "Nadaprabhu Kempegowda Station, Majestic",
    50,
)


def main():
    passed = 0
    for desc, src, dst, expected in CASES:
        try:
            result = calculate_fare(src, dst)
        except Exception as e:
            print(f"FAIL  {desc}\n      -> error: {e}")
            continue
        actual = result['fare']
        km = result['distance_km']
        ok = abs(actual - expected) <= TOLERANCE
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"{status}  {desc}")
        print(f"      {src}  ->  {dst}")
        print(f"      distance={km} km   fare=Rs.{actual}   expected~Rs.{expected}   interchanges={result['interchanges']}")
    print(f"\n{passed}/{len(CASES)} passed (tolerance +/- Rs.{TOLERANCE})")


if __name__ == '__main__':
    main()
