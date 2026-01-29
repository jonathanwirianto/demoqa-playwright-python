import os
from playwright.sync_api import expect
from utils import generate_unique_user, take_screenshot

REGISTER_URL = "https://demoqa.com/register"


def test_register_page_elements(page, request):
    page.goto(REGISTER_URL, wait_until="domcontentloaded")

    expect(page.locator("#firstname")).to_be_visible()
    expect(page.locator("#lastname")).to_be_visible()
    expect(page.locator("#userName")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.get_by_role("button", name="Register")).to_be_visible()
    expect(page.get_by_role("button", name="Back to Login")).to_be_visible()

    take_screenshot(page, request.node.name)


def test_register_with_valid_unique_data_without_captcha(page, request):
    user = generate_unique_user()

    page.goto(REGISTER_URL, wait_until="domcontentloaded")

    page.locator("#firstname").fill(user["first_name"])
    page.locator("#lastname").fill(user["last_name"])
    page.locator("#userName").fill(user["username"])
    page.locator("#password").fill(user["password"])

    page.get_by_role("button", name="Register").click()

    # CAPTCHA error is expected
    error_message = page.locator("#name")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Please verify reCaptcha to register!")

    take_screenshot(page, request.node.name)


def test_register_existing_user_shows_error_without_captcha(page, request):
    username = os.getenv("DEMOQA_USERNAME")

    page.goto(REGISTER_URL, wait_until="domcontentloaded")

    page.locator("#firstname").fill("Existing")
    page.locator("#lastname").fill("User")
    page.locator("#userName").fill(username)
    page.locator("#password").fill("TestPassword123!")

    page.get_by_role("button", name="Register").click()

    error_message = page.locator("#name")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Please verify reCaptcha to register!")

    take_screenshot(page, request.node.name)


def test_register_missing_required_fields(page, request):
    page.goto(REGISTER_URL, wait_until="domcontentloaded")

    page.get_by_role("button", name="Register").click()

    # Still on register page
    expect(page).to_have_url(REGISTER_URL)

    take_screenshot(page, request.node.name)
