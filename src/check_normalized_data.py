import json


FILE = "data/processed/normalized_schemes.json"


with open(FILE, "r", encoding="utf-8") as file:
    schemes = json.load(file)


print("Total schemes:", len(schemes))

print("\nDistrict examples:")

for scheme in schemes:

    if scheme.get("districts"):

        print(
            scheme["scheme_name"],
            "=>",
            scheme["districts"]
        )

        break