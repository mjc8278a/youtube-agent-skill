#!/usr/bin/env python3
"""Validate creator-provided CSV snapshots and emit offline per-post metrics as JSON."""
import argparse
import csv
from datetime import datetime
import json
import math
from pathlib import Path
import sys

REQUIRED = {"video_id", "posted_at", "observed_at", "duration_seconds", "views"}
COUNTS = ("views", "likes", "comments", "shares", "saves", "complete_views", "new_followers")


def number(value, field, integer=False, required=False):
    value = (value or "").strip()
    if not value:
        if required:
            raise ValueError(f"{field} is required")
        return None
    if integer:
        if not value.isascii() or not value.isdecimal():
            raise ValueError(f"{field} must be a nonnegative integer")
        return int(value)
    try:
        result = float(value)
    except ValueError:
        raise ValueError(f"{field} must be numeric") from None
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{field} must be finite and nonnegative")
    return result


def timestamp(value, field):
    try:
        result = datetime.fromisoformat((value or "").strip().replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"{field} must be an ISO timestamp with timezone") from None
    if result.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone")
    return result


def percent(numerator, denominator):
    return None if numerator is None or not denominator else round(100 * numerator / denominator, 4)


def analyze(path):
    output, seen = [], set()
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError("duplicate CSV header")
        missing = REQUIRED - set(fields)
        if missing:
            raise ValueError("missing columns: " + ", ".join(sorted(missing)))
        for line, row in enumerate(reader, 2):
            try:
                if None in row:
                    raise ValueError("more values than CSV columns")
                video_id = (row.get("video_id") or "").strip()
                if not video_id:
                    raise ValueError("video_id is required")
                posted = timestamp(row.get("posted_at"), "posted_at")
                observed = timestamp(row.get("observed_at"), "observed_at")
                if observed < posted:
                    raise ValueError("observed_at precedes posted_at")
                key = (video_id, observed)
                if key in seen:
                    raise ValueError("duplicate video_id and observed_at snapshot")
                seen.add(key)
                duration = number(row.get("duration_seconds"), "duration_seconds", required=True)
                if duration == 0:
                    raise ValueError("duration_seconds must be positive")
                counts = {field: number(row.get(field), field, integer=True, required=field == "views")
                          for field in COUNTS}
                views = counts["views"]
                completed = counts["complete_views"]
                if completed is not None and completed > views:
                    raise ValueError("complete_views exceeds views; check metric definitions")
                watch = number(row.get("avg_watch_seconds"), "avg_watch_seconds")
                actions = [counts[field] for field in ("likes", "comments", "shares", "saves")]
                engagement = None if None in actions else sum(actions)
                distribution = (row.get("distribution") or "unknown").strip() or "unknown"
                if distribution not in {"organic", "paid", "unknown"}:
                    raise ValueError("distribution must be organic, paid or unknown")
                output.append({
                    "video_id": video_id, "posted_at": posted.isoformat(),
                    "observed_at": observed.isoformat(),
                    "age_hours": round((observed - posted).total_seconds() / 3600, 4),
                    "duration_seconds": duration, **counts, "avg_watch_seconds": watch,
                    "format": (row.get("format") or "").strip(),
                    "distribution": distribution,
                    "experiment": (row.get("experiment") or "").strip(),
                    "engagement_per_view_pct": percent(engagement, views),
                    "share_per_view_pct": percent(counts["shares"], views),
                    "save_per_view_pct": percent(counts["saves"], views),
                    "follower_per_view_pct": percent(counts["new_followers"], views),
                    "completion_pct": percent(completed, views),
                    "watch_ratio_pct": percent(watch, duration),
                })
            except (ValueError, OverflowError) as exc:
                raise ValueError(f"row {line}: {exc}") from None
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="creator-provided snapshot CSV")
    args = parser.parse_args()
    try:
        result = analyze(args.csv)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, csv.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
