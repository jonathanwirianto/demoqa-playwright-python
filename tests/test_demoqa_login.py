import os
from playwright.sync_api import expect
from utils import take_screenshot

LOGIN_URL = "https://demoqa.com/login"
PROFILE_URL = "https://demoqa.com/profile"
REGISTER_URL = "https://demoqa.com/register"

def get_credentials():
    username = os.getenv("DEMOQA_USERNAME")
    password = os.getenv("DEMOQA_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Missing DEMOQA_USERNAME / DEMOQA_PASSWORD in environment"
        )

    return username, password

def test_login_page_elements(page, request):
    page.goto(LOGIN_URL, wait_until="domcontentloaded")

    expect(page.locator("#userName-label")).to_be_visible()
    expect(page.locator("#password-label")).to_be_visible()
    expect(page.locator("#userName")).to_be_visible()
    expect(page.locator("#password")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    expect(page.get_by_role("button", name="New User")).to_be_visible()

    take_screenshot(page=page, test_name=request.node.name)

def test_login_valid_user(page, request):
    username, password = get_credentials()

    page.goto(LOGIN_URL, wait_until="domcontentloaded")

    page.locator("#userName").fill(username)
    page.locator("#password").fill(password)
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(PROFILE_URL)

    # Validate username on profile
    expect(page.get_by_text(username)).to_be_visible()

    take_screenshot(page=page, test_name=request.node.name)



def test_login_non_existing_user(page, request):
    page.goto(LOGIN_URL, wait_until="domcontentloaded")

    page.locator("#userName").fill("non_existing_user_12345")
    page.locator("#password").fill("wrong_password_12345")
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Invalid", exact=False)).to_be_visible()

    error_message = page.locator("#name")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Invalid username or password!")

    # Still on login page
    expect(page).to_have_url(LOGIN_URL)

    take_screenshot(page=page, test_name=request.node.name)



def test_login_empty_fields(page, request):
    page.goto(LOGIN_URL, wait_until="domcontentloaded")

    page.get_by_role("button", name="Login").click()

    # Still on login page
    expect(page).to_have_url(LOGIN_URL)

    take_screenshot(page=page, test_name=request.node.name)

def test_click_register_button(page, request):
    page.goto(LOGIN_URL,wait_until="domcontentloaded")

    page.get_by_role("button", name="New User").click()

    # Go to register page
    expect(page).to_have_url(REGISTER_URL)

    take_screenshot(page=page, test_name=request.node.name)
