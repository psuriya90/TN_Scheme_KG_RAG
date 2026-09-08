import json

FILE = "data/processed/schemes.json"

with open(FILE, "r", encoding="utf-8") as file:
    schemes = json.load(file)

print("=" * 60)
print("DATA VALIDATION")
print("=" * 60)

print("Total schemes:", len(schemes))

successful = 0
failed = 0

for scheme in schemes:

    if scheme.get("error"):
        failed += 1
    else:
        successful += 1

print("Successful:", successful)
print("Failed:", failed)

print("\nFirst scheme:")
print("=" * 60)

first = schemes[0]

for key, value in first.items():
    print(f"\n{key}:")
    print(value)