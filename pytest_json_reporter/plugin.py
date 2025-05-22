import os

import pytest

import pytest
import json

from pytest_json_reporter.reporter import JSONReporter
test_screenshot_paths = {}
reporter = JSONReporter()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" or (report.when == "setup" and report.skipped):
        config = item.config
        capture_option = config.getoption("--capture-screenshots")
        tool = config.getoption("--automation-tool")

        should_capture = (
            capture_option == "all" or
            (capture_option == "failed" and report.outcome == "failed")
        )

        screenshot_path = None
        if should_capture:
            print('capture')
            driver = None
            print(tool)
            if tool == "playwright":

                driver = item.funcargs.get("page", None)
                print(driver)
            else:
                driver = item.funcargs.get("driver", None)

            if driver:
                print(driver)
                screenshot_path = take_screenshot_on_failure(item, driver)

        reporter.log_result(
            test_name=item.name,
            nodeid=item.nodeid,
            status=report.outcome,
            duration=report.duration,
            error=str(report.longrepr) if report.failed else None,
            markers=[m.name for m in item.iter_markers()],
            filepath=item.location[0],
            lineno=item.location[1],
            stdout=getattr(report, "capstdout", ""),
            stderr=getattr(report, "capstderr", ""),
            screenshot=screenshot_path,
        )


def pytest_sessionfinish(session, exitstatus):
    reporter.write_report()

def pytest_load_initial_conftests(args):
    if not any(arg.startswith("--capture") for arg in args):
        args.append("--capture=tee-sys")

def pytest_addoption(parser):
    parser.addoption(
        "--json-report",
        action="store",
        default="report.json",
        help="Path to save the JSON test report"
    )
    parser.addoption(
        "--automation-tool",
        action="store",
        default="playwright",
        choices=["selenium", "playwright"],
        help="Specify automation tool: selenium (default) or playwright"
    )
    parser.addoption(
        "--capture-screenshots",
        action="store",
        default="failed",
        choices=["failed", "all", "none"],
        help="Capture screenshots: failed (default), all, or none"
    )

import os

def take_screenshot_on_failure(item, page):
    print("✅ take_screenshot_on_failure was called")
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    filename = f"{item.name}.png".replace("/", "_").replace("\\", "_")
    path = os.path.join(screenshot_dir, filename)
    # Assuming sync call here, adjust if async
    page.screenshot(path=path)
    return path

def take_screenshot_selenium(item, driver):
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    filename = f"{item.name}.png".replace("/", "_").replace("\\", "_")
    path = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(path)
    return path


