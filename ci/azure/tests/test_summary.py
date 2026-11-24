"""Unit tests for ci/azure/summary.py (run summary rendering)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import summary  # noqa: E402

MATRIX = {
    "poky_qemux86_64_scarthgap": {"BSP_NAME": "poky-qemux86-64-scarthgap"},
    "poky_harden_qemux86_64_scarthgap": {"BSP_NAME": "poky-harden-qemux86-64-scarthgap"},
    "rock_5b_wrynose": {"BSP_NAME": "rock-5b-wrynose"},
    "jetson_x": {"BSP_NAME": "jetson-x"},
}

RECORDS = [
    {"type": "Job", "id": "j1", "name": "Build BSP poky_qemux86_64_scarthgap",
     "result": "succeeded", "attempt": 1,
     "startTime": "2026-11-23T10:00:00.1234567Z", "finishTime": "2026-11-23T12:34:56.9999999Z"},
    {"type": "Task", "id": "t1", "parentId": "j1", "name": "Deploy artifacts", "result": "succeeded"},
    {"type": "Job", "id": "j2", "name": "Build BSP poky_harden_qemux86_64_scarthgap",
     "result": "failed", "attempt": 2,
     "startTime": "2026-11-23T10:00:00Z", "finishTime": "2026-11-23T10:07:30Z"},
    {"type": "Job", "id": "j3", "name": "Build BSP rock_5b_wrynose", "result": "canceled",
     "startTime": "2026-11-23T10:00:00Z", "finishTime": "2026-11-23T10:08:00Z"},
]


class RenderTest(unittest.TestCase):
    def table_rows(self, text):
        return [l for l in text.splitlines() if l.startswith("| `")]

    def test_empty_matrix(self):
        self.assertIn("No presets were selected", summary.render({}, [], False, False, False))

    def test_rows_failures_first_and_suffix_match_is_exact(self):
        text = summary.render(MATRIX, RECORDS, False, False, False)
        rows = self.table_rows(text)
        self.assertEqual(len(rows), 4)
        self.assertIn("poky-harden-qemux86-64-scarthgap", rows[0])
        self.assertIn("Failed", rows[0])
        self.assertIn("failure-logs-poky-harden-qemux86-64-scarthgap-2", rows[0])
        self.assertIn("Canceled", rows[1])
        self.assertIn("Not run", rows[2])
        self.assertIn("poky-qemux86-64-scarthgap", rows[3])
        self.assertIn("Succeeded", rows[3])

    def test_durations(self):
        text = summary.render(MATRIX, RECORDS, False, False, False)
        self.assertIn("2h 34m", text)
        self.assertIn("7m 30s", text)

    def test_deploy_column_only_when_deploying(self):
        self.assertNotIn("| Deploy |", summary.render(MATRIX, RECORDS, False, False, False))
        text = summary.render(MATRIX, RECORDS, False, True, False)
        self.assertIn("| Deploy |", text)

    def test_mode_line(self):
        text = summary.render(MATRIX, RECORDS, True, False, True)
        self.assertIn("Check only", text)
        self.assertIn("pull request", text)

    def test_repo_overrides_line(self):
        self.assertNotIn("Repo overrides", summary.render(MATRIX, RECORDS, False, False, False))
        text = summary.render(MATRIX, RECORDS, False, False, False, ["meta-a@x", "poky@tag:v1"])
        self.assertIn("**Repo overrides:** `meta-a@x`, `poky@tag:v1`", text)

    def test_counts(self):
        text = summary.render(MATRIX, RECORDS, False, False, False)
        self.assertIn("1 failed, 1 canceled, 1 not run, 1 succeeded", text)


if __name__ == "__main__":
    unittest.main()
