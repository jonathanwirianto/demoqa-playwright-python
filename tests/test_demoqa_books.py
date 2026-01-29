from playwright.sync_api import expect
import re

BASE_URL = "https://demoqa.com/books"

def test_books_page_elements(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")

    expect(page).to_have_title("DEMOQA")
    expect(page.get_by_text("Book Store", exact=True)).to_be_visible()
    expect(page.get_by_placeholder("Type to search")).to_be_visible()

    page.screenshot(path="artifacts/screenshots/books_smoke.png", full_page=True)


def test_books_search_filters_results(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")

    search = page.get_by_placeholder("Type to search")
    search.fill("Git Pocket")

    expect(page.get_by_role("link", name="Git Pocket Guide")).to_be_visible()

    page.screenshot(path="artifacts/screenshots/books_search_git_pocket.png", full_page=True)


def test_open_book_details(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")

    page.get_by_role("link", name="Git Pocket Guide").click()
    
    expect(page).to_have_url(re.compile(r".*\bbook=\d+.*"))
    # Only verify url because details page currently only show blank page (not clear it is expected or not)

    page.screenshot(path="artifacts/screenshots/book_details_git_pocket.png", full_page=True)


def test_rows_per_page_changes_row_count(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")

    rows_select = page.locator("select").first
    expect(rows_select).to_be_visible()

    rows_select.select_option("5")

    rows = page.locator(".rt-tbody .rt-tr-group")
    expect(rows).to_have_count(5)

    page.screenshot(path="artifacts/screenshots/books_rows_per_page_5.png", full_page=True)

def test_books_pagination_next_after_setting_rows_to_5(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")

    #Set row to 5
    rows_select = page.locator("select").first
    expect(rows_select).to_be_visible()
    rows_select.select_option("5")

    expect(page.get_by_role("link", name="Git Pocket Guide")).to_be_visible()

    next_button = page.get_by_role("button", name="Next")
    expect(next_button).to_be_visible()
    next_button.click()

    #Verify a known page 2 book appears
    expect(
        page.get_by_role("link", name="Programming JavaScript Application")
    ).to_be_visible()

    page.screenshot(
        path="artifacts/screenshots/books_rows_5_next_page.png",
        full_page=True
    )
