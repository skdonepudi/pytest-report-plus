import io
import os
import shutil
import subprocess
import warnings

import pytest

import pytest
import json

from pytest_json_reporter.generate_html_report import JSONReporter
python_executable = shutil.which("python3") or shutil.which("python")
test_screenshot_paths = {}
reporter = JSONReporter()

import logging

logger = logging.getLogger()  # root logger
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if "caplog" not in item.fixturenames:
        item.fixturenames.append("caplog")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" or (report.when == "setup" and report.skipped):
        config = item.config
        capture_option = config.getoption("--capture-screenshots")
        tool = config.getoption("--automation-tool")

        caplog_text = None
        if "caplog" in item.funcargs:
            caplog = item.funcargs["caplog"]
            caplog_text = "\n".join(caplog.messages) if caplog.messages else None

        screenshot_path = None
        should_capture_screenshot = (
            capture_option == "all" or
            (capture_option == "failed" and report.outcome == "failed")
        )

        if should_capture_screenshot:
            driver = item.funcargs.get("page" if tool == "playwright" else "driver", None)
            if driver:
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
            logs=caplog_text
        )

import subprocess


def pytest_sessionfinish(session, exitstatus):
    print("pytest_sessionfinish called")
    reporter.write_report()

    json_path = session.config.getoption("--json-report")
    html_output = session.config.getoption("--html-output")
    screenshots = session.config.getoption("--screenshots")

    # Resolve absolute path of the generate_html_report.py script relative to this file
    script_path = os.path.join(os.path.dirname(__file__), "generate_html_report.py")

    if not os.path.exists(script_path):
        print(f"Warning: Report generation script not found at {script_path}. Skipping HTML report generation.")
        return

    try:
        subprocess.run([
            python_executable,
            script_path,
            "--report", json_path,
            "--screenshots", screenshots,
            "--output", html_output
        ], check=True)
    except Exception as e:
        print(f"Exception during HTML report generation: {e}")

def pytest_sessionstart(session):
    configure_logging()
    print("Plugin loaded: pytest_sessionstart called")

def pytest_runtest_logreport(report):
    print(f"pytest_runtest_logreport: {report.nodeid} - {report.outcome}")

def pytest_load_initial_conftests(args):
    if not any(arg.startswith("--capture") for arg in args):
        args.append("--capture=tee-sys")

def pytest_addoption(parser):
    parser.addoption(
        "--json-report",
        action="store",
        default="playwright_report.json",
        help="Directory to save individual JSON test reports"
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
    parser.addoption("--html-output", default="report_output")
    parser.addoption("--screenshots", default="screenshots")

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

import logging
import sys

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if rerun in same session
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

