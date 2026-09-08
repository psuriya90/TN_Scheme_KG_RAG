from playwright.sync_api import sync_playwright


URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening website...")

    page.goto(
        URL,
        wait_until="networkidle",
        timeout=60000
    )

    print("\nPAGE TITLE:")
    print(page.title())

    print("\nURL:")
    print(page.url)

    # Get all links
    links = page.locator("a")

    print("\nTOTAL LINKS:", links.count())

    for i in range(links.count()):

        link = links.nth(i)

        text = link.inner_text().strip()

        href = link.get_attribute("href")

        if text:
            print(f"\nLINK {i}")
            print("TEXT :", text)
            print("HREF :", href)

    # Save complete HTML
    html = page.content()

    with open(
        "data/raw/scheme_page.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    print("\nHTML saved to:")
    print("data/raw/scheme_page.html")

    browser.close()