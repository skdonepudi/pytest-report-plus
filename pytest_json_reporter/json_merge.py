import json
import os


def merge_json_reports(directory=".pytest_worker_jsons", output_path="playwright_report.json"):
    merged_results = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename)) as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):  # assuming each report is a list of tests
                        merged_results.extend(data)
                    elif isinstance(data, dict) and "results" in data:
                        merged_results.extend(data["results"])
                except Exception as e:
                    print(f"⚠️ Could not parse {filename}: {e}")

    with open(output_path, "w") as f:
        json.dump(merged_results, f, indent=2)
    print(f"✅ Merged report written to {output_path}")
