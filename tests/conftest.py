import os
import pytest
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

@pytest.fixture
def page(request):
    video_dir = "artifacts/videos"
    os.makedirs(video_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1366, "height": 900},
            record_video_dir=video_dir
        )
        page = context.new_page()
        yield page

        # Finalize video
        context.close()
        browser.close()

        video = page.video
        if video:
            original = video.path()
            new_name = f"{request.node.name}_{timestamp()}.webm"
            new_path = os.path.join(video_dir, new_name)

            if os.path.exists(original):
                os.rename(original, new_path)
