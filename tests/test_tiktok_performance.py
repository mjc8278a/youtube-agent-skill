"""Behavioral checks for offline TikTok snapshot calculations and CLI failure paths."""
import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/tiktok-creator/scripts/performance.py"
spec = importlib.util.spec_from_file_location("performance", SCRIPT)
performance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(performance)
FIELDS = (ROOT / "skills/tiktok-creator/assets/performance.csv").read_text().strip().split(",")


class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "snapshots.csv"
        self.row = dict(video_id="fictional-1", posted_at="2026-11-01T12:00:00-05:00",
                        observed_at="2026-11-02T17:00:00Z", duration_seconds="20",
                        views="100", likes="10", comments="2", shares="3", saves="5",
                        complete_views="40", new_followers="2", avg_watch_seconds="25",
                        format="solo-sketch", distribution="organic", experiment="short-setup")

    def write(self, rows):
        with self.path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_rates_and_replay(self):
        self.write([self.row])
        result = performance.analyze(self.path)[0]
        self.assertEqual(result["age_hours"], 24)
        for key, value in {"engagement_per_view_pct": 20, "share_per_view_pct": 3,
                           "save_per_view_pct": 5, "follower_per_view_pct": 2,
                           "completion_pct": 40, "watch_ratio_pct": 125}.items():
            self.assertEqual(result[key], value)

    def test_missing_counts_are_unknown_and_zero_is_known(self):
        self.write([{**self.row, "saves": "", "shares": "0", "complete_views": ""}])
        result = performance.analyze(self.path)[0]
        self.assertIsNone(result["engagement_per_view_pct"])
        self.assertIsNone(result["save_per_view_pct"])
        self.assertIsNone(result["completion_pct"])
        self.assertEqual(result["share_per_view_pct"], 0)

    def test_zero_views(self):
        self.write([{**self.row, **{field: "0" for field in performance.COUNTS}}])
        result = performance.analyze(self.path)[0]
        self.assertIsNone(result["engagement_per_view_pct"])
        self.assertIsNone(result["completion_pct"])

    def test_invalid_rows(self):
        for changes in ({"views": "-1"}, {"views": "1.5"}, {"views": ""},
                        {"duration_seconds": "0"}, {"duration_seconds": "NaN"},
                        {"avg_watch_seconds": "inf"}, {"avg_watch_seconds": "-1"},
                        {"complete_views": "101"}, {"video_id": ""},
                        {"distribution": "boostedish"},
                        {"posted_at": "2026-11-01T12:00:00"},
                        {"observed_at": "2020-01-01T00:00:00Z"}):
            with self.subTest(changes=changes):
                self.write([{**self.row, **changes}])
                with self.assertRaisesRegex(ValueError, "row 2"):
                    performance.analyze(self.path)

    def test_duplicate_instant_rejected_even_across_timezones(self):
        self.write([self.row, {**self.row, "observed_at": "2026-11-02T12:00:00-05:00"}])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            performance.analyze(self.path)

    def test_distinct_snapshots_retained(self):
        self.write([self.row, {**self.row, "observed_at": "2026-11-03T17:00:00Z"}])
        self.assertEqual(len(performance.analyze(self.path)), 2)

    def test_cli_json_and_input_unchanged(self):
        self.write([self.row])
        before = self.path.read_bytes()
        run = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)[0]["views"], 100)
        self.assertEqual(self.path.read_bytes(), before)

    def test_cli_failure_without_partial_results(self):
        self.write([self.row, {**self.row, "views": "bad"}])
        run = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, "")
        self.assertIn("row 3", run.stderr)

    def test_headers_and_empty_template(self):
        self.write([])
        self.assertEqual(performance.analyze(self.path), [])
        for bad in ("video_id,views\nx,2\n", "video_id,video_id\nx,x\n"):
            self.path.write_text(bad)
            with self.assertRaises(ValueError):
                performance.analyze(self.path)


if __name__ == "__main__":
    unittest.main()
