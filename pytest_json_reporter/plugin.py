import pytest

import pytest
import json

from pytest_json_reporter.reporter import JSONReporter

reporter = JSONReporter()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        error = str(report.longrepr) if report.failed else None
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
        )

def pytest_sessionfinish(session, exitstatus):
    reporter.write_report()

