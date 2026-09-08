from playwright.sync_api import sync_playwright


URL = (
    "https://www.tn.gov.in/"
    "scheme_details.php?id=MTU2Ng=="
)


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("Opening scheme page...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    print("\nTITLE:")
    print(page.title())

    print("\nCURRENT URL:")
    print(page.url)

    print("\nPAGE TEXT:")
    print("=" * 80)

    print(
        page.locator("body").inner_text()
    )

    print("=" * 80)

    # Save HTML
    html = page.content()

    with open(
        "data/raw/training_to_farmers.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    # Screenshot
    page.screenshot(
        path="data/raw/training_to_farmers.png",
        full_page=True
    )

    print("\nHTML saved.")

    print(
        "Screenshot saved."
    )

    browser.close()