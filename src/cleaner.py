import json
import re
from pathlib import Path


INPUT_FILE = Path("data/processed/schemes.json")
OUTPUT_FILE = Path("data/processed/cleaned_schemes.json")


# ---------------------------------------------------------
# Districts in Tamil Nadu
# ---------------------------------------------------------

TAMIL_NADU_DISTRICTS = [
    "Ariyalur",
    "Chengalpattu",
    "Chennai",
    "Coimbatore",
    "Cuddalore",
    "Dharmapuri",
    "Dindigul",
    "Erode",
    "Kallakurichi",
    "Kancheepuram",
    "Karur",
    "Krishnagiri",
    "Madurai",
    "Mayiladuthurai",
    "Nagapattinam",
    "Namakkal",
    "Nilgiris",
    "Perambalur",
    "Pudukkottai",
    "Ramanathapuram",
    "Ranipet",
    "Salem",
    "Sivaganga",
    "Tenkasi",
    "Thanjavur",
    "Theni",
    "Thoothukudi",
    "Tiruchirappalli",
    "Tirunelveli",
    "Tirupathur",
    "Tiruppur",
    "Tiruvallur",
    "Tiruvarur",
    "Vellore",
    "Viluppuram",
    "Virudhunagar",
]

def clean_text(value):
    """
    Clean unnecessary whitespace.
    """

    if not value:
        return ""

    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def extract_districts(text):
    """
    Extract Tamil Nadu districts mentioned in
    the scheme description.
    """

    districts = []

    text_lower = text.lower()

    for district in TAMIL_NADU_DISTRICTS:

        if district.lower() in text_lower:

            districts.append(district)

    return districts


def process_scheme(scheme):

    description = clean_text(
        scheme.get("description", "")
    )

    cleaned = {
        "department": clean_text(
            scheme.get("department", "")
        ),

        "district": clean_text(
            scheme.get("concerned_district", "")
        ),

        "organisation": clean_text(
            scheme.get("organisation_name", "")
        ),

        "scheme_name": clean_text(
            scheme.get("scheme_name", "")
        ),

        "associated_scheme": clean_text(
            scheme.get("associated_scheme", "")
        ),

        "sponsored_by": clean_text(
            scheme.get("sponsored_by", "")
        ),

        "funding_pattern": clean_text(
            scheme.get("funding_pattern", "")
        ),

        "beneficiaries": clean_text(
            scheme.get("beneficiaries", "")
        ),

        "benefits": clean_text(
            scheme.get("types_of_benefits", "")
        ),

        "eligibility": clean_text(
            scheme.get("eligibility_criteria", "")
        ),

        "income": clean_text(
            scheme.get("income", "")
        ),

        "age_from": clean_text(
            scheme.get("age_from", "")
        ),

        "age_to": clean_text(
            scheme.get("age_to", "")
        ),

        "community": clean_text(
            scheme.get("community", "")
        ),

        "how_to_avail": clean_text(
            scheme.get("how_to_avail", "")
        ),

        "validity": clean_text(
            scheme.get("validity", "")
        ),

        "introduced_on": clean_text(
            scheme.get("introduced_on", "")
        ),

        "description": description,

        "scheme_type": clean_text(
            scheme.get("scheme_type", "")
        ),

        "uploaded_file": clean_text(
            scheme.get("uploaded_file", "")
        ),

        "source_url": clean_text(
            scheme.get("source_url", "")
        ),

        # ---------------------------------------------
        # Knowledge Graph specific information
        # ---------------------------------------------

        "districts": extract_districts(description),

    }

    return cleaned


def main():

    print("=" * 70)
    print("TN SCHEME DATA CLEANER")
    print("=" * 70)

    # Load scraped data
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    print(
        f"\nLoaded schemes: {len(schemes)}"
    )

    cleaned_schemes = []

    for scheme in schemes:

        cleaned = process_scheme(
            scheme
        )

        cleaned_schemes.append(
            cleaned
        )

    # Save cleaned data
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cleaned_schemes,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"\nCleaned schemes: {len(cleaned_schemes)}"
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )

    # Display first scheme
    print("\n" + "=" * 70)
    print("FIRST CLEANED SCHEME")
    print("=" * 70)

    first = cleaned_schemes[0]

    for key, value in first.items():

        print(f"\n{key}:")
        print(value)


if __name__ == "__main__":
    main()