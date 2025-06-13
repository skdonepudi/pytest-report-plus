import json
import os
import shutil
import tempfile

import pytest

from pytest_reporter_plus.json_merge import merge_json_reports


class TestMergeJsonReports:
    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.test_dir)

    def _write_json(self, filename, content):
        path = os.path.join(self.test_dir, filename)
        with open(path, "w") as f:
            json.dump(content, f)

    def test_merges_multiple_jsons_with_same_nodeid(self):
        data1 = [{"nodeid": "test_sample.py::test_case", "status": "failed"}]
        data2 = [{"nodeid": "test_sample.py::test_case", "status": "passed"}]

        self._write_json("part1.json", data1)
        self._write_json("part2.json", data2)

        output_path = os.path.join(self.test_dir, "merged.json")
        merge_json_reports(directory=self.test_dir, output_path=output_path)

        with open(output_path) as f:
            merged = json.load(f)

        print(merged)
        assert len(merged) == 1
        assert merged[0]["nodeid"] == "test_sample.py::test_case"
        assert merged[0]["status"] in ["passed", "failed"]  # if order isn't guaranteed
        assert set(merged[0]["flaky_attempts"]) == {"passed", "failed"}
        assert merged[0]["flaky"] is True

    def test_fallback_to_test_key(self):
        # If only "test" key is present (not "nodeid"), it should still group correctly
        data1 = [{"test": "test_sample.py::test_alt", "status": "skipped"}]
        data2 = [{"test": "test_sample.py::test_alt", "status": "passed"}]

        self._write_json("p1.json", data1)
        self._write_json("p2.json", data2)

        output_path = os.path.join(self.test_dir, "merged_alt.json")
        merge_json_reports(directory=self.test_dir, output_path=output_path)

        with open(output_path) as f:
            merged = json.load(f)

        assert len(merged) == 1
        assert merged[0]["test"] == "test_sample.py::test_alt"
        assert merged[0]["status"] == "passed"
        assert merged[0]["flaky"] is True
        assert merged[0]["flaky_attempts"] == ["skipped", "passed"]

    def test_ignores_invalid_json(self):
        # Write a corrupt file
        bad_path = os.path.join(self.test_dir, "broken.json")
        with open(bad_path, "w") as f:
            f.write("{ not valid json")

        # Write a valid file
        good_data = [{"nodeid": "test_x.py::test_y", "status": "passed"}]
        self._write_json("good.json", good_data)

        output_path = os.path.join(self.test_dir, "merged.json")
        merge_json_reports(directory=self.test_dir, output_path=output_path)

        with open(output_path) as f:
            merged = json.load(f)

        assert len(merged) == 1
        assert merged[0]["status"] == "passed"
