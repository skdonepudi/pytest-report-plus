import pytest

@pytest.mark.smoke
def test_example_failed(page):
    page.goto("https://example.com")
    title = page.title()
    print("this shud come")
    assert "Example Domain" in title

@pytest.mark.regression
def test_example_passed(page):
    page.goto("https://example.com")
    title = page.title()
    assert "Example Domain" in title

@pytest.mark.production
def test_example_longest_running_passed(page):
    page.goto("https://example.com")
    title = page.title()
    assert "Example Domain" in title

@pytest.mark.regression
def test_example_longest_running_failed(page):
    page.goto("https://example.com")
    title = page.title()
    assert "Example Domain" in title