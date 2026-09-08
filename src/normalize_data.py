import json
import os


INPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "processed",
    "cleaned_schemes.json"
)

OUTPUT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "processed",
    "normalized_schemes.json"
)


DISTRICT_ALIASES = {
    "Trichy": "Tiruchirappalli",
    "Villupuram": "Viluppuram",
    "Sivagangai": "Sivaganga",
}


def normalize_districts(districts):

    normalized = []

    for district in districts:

        district = district.strip()

        if not district:
            continue

        district = DISTRICT_ALIASES.get(
            district,
            district
        )

        if district not in normalized:
            normalized.append(district)

    return normalized


def normalize_schemes():

    print("Loading cleaned scheme data...")

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    print(f"Loaded {len(schemes)} schemes.")

    for scheme in schemes:

        districts = scheme.get("districts", [])

        scheme["districts"] = normalize_districts(
            districts
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            schemes,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("Normalization completed.")
    print(f"Saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":

    normalize_schemes()