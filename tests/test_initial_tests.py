import pytest
def test_initial():
    assert True

@pytest.mark.link("https://jira.company.com/testcase/1234")
def test_show_link():
        assert True

@pytest.mark.link("https://jira.company.com/testcase/1234")
@pytest.mark.link("https://jira.company.com/testcase/12345")
def test_show_multiplelinks():
        assert True
