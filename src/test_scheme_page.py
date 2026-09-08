from playwright.sync_api import sync_playwright


URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("Opening website...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    print("\nTITLE:")
    print(page.title())

    print("\nURL:")
    print(page.url)

    print("\nPAGE TEXT:")
    print(page.locator("body").inner_text()[:10000])

    page.screenshot(
        path="data/raw/scheme_page.png",
        full_page=True
    )

    browser.close()