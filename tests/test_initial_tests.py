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
    print('this appears')


@pytest.mark.link("https://github.com/reach2jeyan/pytest-reporter-plus/issues/15")
@pytest.mark.testcase("https://github.com/reach2jeyan/pytest-reporter-plus/issues/25")
def test_github_link():
    assert True


@pytest.mark.jira("https://github.com/reach2jeyan/pytest-reporter-plus/issues/25")
def test_github_link_another_case():
    assert True
