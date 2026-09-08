from playwright.sync_api import sync_playwright
import json
from pathlib import Path


URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="


def scrape_scheme_list():

    print("Starting scraper...")

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        print("Opening website...")

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        print("Page loaded successfully.")

        # --------------------------------------------------
        # 1. Extract department name
        # --------------------------------------------------

        department = "Unknown"

        body_text = page.locator("body").inner_text()

        if "Agriculture - Farmers Welfare Department" in body_text:
            department = "Agriculture - Farmers Welfare Department"

        print("\nDepartment:")
        print(department)

        # --------------------------------------------------
        # 2. Find all links
        # --------------------------------------------------

        links = page.locator("a")

        schemes = []

        for i in range(links.count()):

            link = links.nth(i)

            scheme_name = link.inner_text().strip()

            href = link.get_attribute("href")

            # --------------------------------------------------
            # 3. Identify scheme detail links
            # --------------------------------------------------

            if (
                scheme_name
                and href
                and "scheme_details.php?id=" in href
            ):

                # Convert relative URL to absolute URL
                if href.startswith("http"):
                    full_url = href
                else:
                    full_url = "https://www.tn.gov.in/" + href

                scheme = {
                    "department": department,
                    "scheme_name": scheme_name,
                    "url": full_url
                }

                schemes.append(scheme)

        browser.close()

    return schemes


def save_schemes(schemes):

    output_file = Path(
        "data/raw/raw_schemes.json"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            schemes,
            file,
            ensure_ascii=False,
            indent=4
        )

    print("\nData saved to:")
    print(output_file)


if __name__ == "__main__":

    schemes = scrape_scheme_list()

    print("\n--------------------------------")
    print("TOTAL SCHEMES FOUND:", len(schemes))
    print("--------------------------------")

    for index, scheme in enumerate(schemes, start=1):

        print(
            f"{index}. "
            f"{scheme['scheme_name']}"
        )

    save_schemes(schemes)