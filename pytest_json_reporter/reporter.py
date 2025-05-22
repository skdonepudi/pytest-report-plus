import json
from datetime import datetime
import os

class JSONReporter:
    def __init__(self, report_path="playwright_report.json"):
        self.report_path = report_path
        self.results = []

    def log_result(
            self,
            test_name,
            nodeid,
            status,
            duration,
            error=None,
            markers=None,
            filepath=None,
            lineno=None,
            stdout=None,
            stderr=None,
            screenshot=None,
    ):
        result = {
            "test": test_name,
            "nodeid": nodeid,
            "status": status,
            "duration": duration,
            "error": error,
            "markers": markers or [],
            "file": filepath,
            "line": lineno,
            "stdout": stdout,
            "stderr": stderr,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "screenshot" : screenshot
        }
        if error:
            result["error"] = error
        self.results.append(result)

    def write_report(self):
        dir_path = os.path.dirname(self.report_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(self.report_path, "w") as f:
            json.dump(self.results, f, indent=2)