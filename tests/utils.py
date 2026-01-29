from datetime import datetime
import random

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def take_screenshot(page, test_name, folder="artifacts/screenshots", full_page=True):
    filename = f"{folder}/{test_name}_{timestamp()}.png"
    page.screenshot(path=filename, full_page=full_page)
    return filename

def random_suffix(length=6):
    return "".join(str(random.randint(0, 9)) for _ in range(length))

def generate_unique_user():
    suffix = random_suffix()
    return {
        "first_name": f"First_{suffix}",
        "last_name": f"Last_{suffix}",
        "username": f"testuser_{suffix}",
        "password": "testQa123!"
    }

