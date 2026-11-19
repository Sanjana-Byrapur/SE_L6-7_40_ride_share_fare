import math


def parse_trip(text):
    """Parse cab:distance, returning None when the input is invalid."""
    if not isinstance(text, str):
        return None
    try:
        cab, km = text.split(':')
        cab = cab.strip().title()
        distance = float(km)
    except ValueError:
        return None
    if not cab or not math.isfinite(distance) or distance < 0:
        return None
    return cab, distance

def fare_average(fares_csv):
    """Return the floor average of non-negative integer fares, or None."""
    if not isinstance(fares_csv, str):
        return None
    parts = fares_csv.split(',')
    # Bound integer conversion on Python versions without a built-in limit.
    if any(len(part.strip()) > 1000 for part in parts):
        return None
    try:
        values = [int(part) for part in parts]
    except ValueError:
        return None
    if any(value < 0 for value in values):
        return None
    return sum(values) // len(values)

def payable_fare(text):
    """Calculate fare including tax and promo, or None for invalid input."""
    if not isinstance(text, str):
        return None
    try:
        fare_text, promo_text = text.split('|')
        fare, promo = float(fare_text), float(promo_text)
    except ValueError:
        return None
    if not math.isfinite(fare) or not math.isfinite(promo) or fare < 0 or promo < 0:
        return None
    total = fare * 1.18 - promo
    if not math.isfinite(total):
        return None
    return max(total, 0)

def main():
    print("==== Running parse_trip ====")
    user_input = input("Enter cab:distance in km (e.g. sedan:12): ")
    result = parse_trip(user_input)
    print("Cab and Distance:", result)

    print("\n==== Running fare_average ====")
    user_input = input("Enter fares as CSV (e.g. 120,95,210): ")
    result = fare_average(user_input)
    print("Average Fare:", result)

    print("\n==== Running payable_fare ====")
    user_input = input("Enter fare|promo (e.g. 250|30): ")
    result = payable_fare(user_input)
    print("Payable Fare:", result)

if __name__ == "__main__":
    main()
