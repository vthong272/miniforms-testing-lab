import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from urllib.parse import urlencode
from pathlib import Path

import pytest
from selenium import webdriver


SERVER_URL = os.getenv("MINIFORMS_URL", "http://127.0.0.1:8765/")
VARIANT = os.getenv("MINIFORMS_VARIANT", "golden")
BASE_URL = f"{SERVER_URL}{'&' if '?' in SERVER_URL else '?'}{urlencode({'variant': VARIANT})}"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def golden_server():
    if os.getenv("MINIFORMS_URL"):
        yield
        return

    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1", "--directory", str(PROJECT_ROOT / "app")],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            try:
                with urllib.request.urlopen(SERVER_URL, timeout=1) as response:
                    body = response.read()
                    if response.status == 200 and b"MiniForms Testing Lab" in body:
                        break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError(f"Golden server did not start at {SERVER_URL}")
        yield
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


@pytest.fixture(scope="session")
def driver(golden_server):
    with tempfile.TemporaryDirectory(prefix=".selenium-profile-", dir=PROJECT_ROOT) as profile:
        options = webdriver.ChromeOptions()
        options.page_load_strategy = "eager"
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,900")
        options.add_argument(f"--user-data-dir={profile}")
        browser = webdriver.Chrome(options=options)
        browser.set_page_load_timeout(10)
        yield browser
        browser.quit()
