import logging.config
import os
from pathlib import Path

import pytest

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

currdir = str(Path(os.path.dirname(os.path.abspath(__file__))).resolve().parents[0])

dir_path = currdir + "/autologs"

# Make sure the directory to the applogs is valid.  The log wil automatically be created by the logger.
Path(dir_path).mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(dir_path + "/applogs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
@pytest.mark.smoke
def test_example_failed(page):
    page.goto("https://example.com")
    title = page.title()
    print("this shud come")
    logger.info("dfdfd")
    assert "Example Domain" in title

@pytest.mark.regression
def test_example_passed(page):
    page.goto("https://example.com")
    print("in the page")
    title = page.title()
    logger.info(f"getting the title from the logger {title}")
    assert "Example Domain" in title
    print("test complete")

@pytest.mark.production
def test_example_longest_running_passed(page):
    page.goto("https://example.com")
    title = page.title()
    print(f"title is {title}")
    assert "Example Domainn" in title

@pytest.mark.regression
def test_example_longest_running_failed(page):
    page.goto("https://example.com")
    title = page.title()
    print(f"title is {title}")
    page.wait_for_timeout(4000)
    assert "Example Domain" in title


@pytest.mark.regression
@pytest.mark.skip
def test_example_longest_running_skipped(page):
    page.goto("https://example.com")
    title = page.title()
    page.wait_for_timeout(4000)
    assert "Example Domain" in title
