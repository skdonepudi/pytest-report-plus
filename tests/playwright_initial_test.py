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
    print("in the page")
    title = page.title()
    print("getting the title")
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
