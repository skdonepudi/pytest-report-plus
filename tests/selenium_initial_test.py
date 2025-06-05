import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_title_should_pass(driver):
    driver.get("https://example.com")
    assert "Example Domain" in driver.title

def test_text_should_fail(driver):
    driver.get("https://example.com")
    elem = driver.find_element(By.TAG_NAME, "h1")
    assert elem.text == "Not the correct heading"  # This will fail
