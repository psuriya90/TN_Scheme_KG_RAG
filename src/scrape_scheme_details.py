from playwright.sync_api import sync_playwright
import json
from pathlib import Path


BASE_URL = "https://www.tn.gov.in/"
INPUT_FILE = Path("data/raw/raw_schemes.json")
OUTPUT_FILE = Path("data/processed/schemes.json")


def extract_value(lines, label):
    """
    Find a field in the page text and return the text after the label.
    """

    for line in lines:
        line = line.strip()

        if line.startswith(label):
            value = line[len(label):].strip()

            # Remove extra colon if present
            value = value.lstrip(":").strip()

            return value

    return ""


def scrape_scheme(page, scheme):
    """
    Scrape one individual scheme detail page.
    """

    url = scheme["url"]

    print("\n" + "=" * 80)
    print("Scraping:")
    print(scheme["scheme_name"])
    print(url)
    print("=" * 80)

    try:

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        body_text = page.locator("body").inner_text()

        lines = [
            line.strip()
            for line in body_text.splitlines()
            if line.strip()
        ]

        data = {
            "department": extract_value(
                lines,
                "Concerned Department:"
            ),

            "concerned_district": extract_value(
                lines,
                "Concerned District:"
            ),

            "organisation_name": extract_value(
                lines,
                "Organisation Name:"
            ),

            "scheme_name": extract_value(
                lines,
                "Scheme Title/Name:"
            ),

            "associated_scheme": extract_value(
                lines,
                "Associated Scheme:"
            ),

            "sponsored_by": extract_value(
                lines,
                "Sponsered By:"
            ),

            "funding_pattern": extract_value(
                lines,
                "Funding Pattern:"
            ),

            "beneficiaries": extract_value(
                lines,
                "Beneficiaries:"
            ),

            "types_of_benefits": extract_value(
                lines,
                "Types of Benefits:"
            ),

            "eligibility_criteria": extract_value(
                lines,
                "Eligibility criteria:"
            ),

            "income": extract_value(
                lines,
                "Income:"
            ),

            "age_from": extract_value(
                lines,
                "Age From:"
            ),

            "age_to": extract_value(
                lines,
                "Age To:"
            ),

            "community": extract_value(
                lines,
                "Community:"
            ),

            "how_to_avail": extract_value(
                lines,
                "How To avail:"
            ),

            "validity": extract_value(
                lines,
                "Validity of the Scheme:"
            ),

            "introduced_on": extract_value(
                lines,
                "Introduced On:"
            ),

            "description": extract_value(
                lines,
                "Description:"
            ),

            "scheme_type": extract_value(
                lines,
                "Scheme Type:"
            ),

            "uploaded_file": extract_value(
                lines,
                "Uploaded File:"
            ),

            "source_url": page.url
        }

        print("Successfully scraped.")

        print("\nScheme Name:")
        print(data["scheme_name"])

        print("\nBeneficiaries:")
        print(data["beneficiaries"])

        print("\nBenefits:")
        print(data["types_of_benefits"])

        print("\nDescription:")
        print(data["description"][:300])

        return data

    except Exception as e:

        print("ERROR:")
        print(e)

        return {
            "department": scheme.get("department", ""),
            "scheme_name": scheme.get("scheme_name", ""),
            "source_url": url,
            "error": str(e)
        }


def main():

    print("=" * 80)
    print("Tamil Nadu Government Scheme Detail Scraper")
    print("=" * 80)

    # --------------------------------------------------
    # Load scheme list
    # --------------------------------------------------

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        schemes = json.load(file)

    print(f"\nTotal schemes to scrape: {len(schemes)}")

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # --------------------------------------------------
        # Scrape every scheme
        # --------------------------------------------------

        for index, scheme in enumerate(schemes, start=1):

            print(
                f"\n[{index}/{len(schemes)}]"
            )

            data = scrape_scheme(
                page,
                scheme
            )

            results.append(data)

        browser.close()

    # --------------------------------------------------
    # Save processed data
    # --------------------------------------------------

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
            results,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\n" + "=" * 80)
    print("SCRAPING COMPLETED")
    print("=" * 80)

    print(f"Total records: {len(results)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()