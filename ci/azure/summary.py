#!/usr/bin/env python3
"""Write the one-page run summary for azure-pipelines.yml.

Reads the run's timeline through the Azure DevOps REST API (with
System.AccessToken), renders a markdown table of every preset in the build
matrix (result, duration, deploy outcome, failure-logs artifact) and attaches
it to the run's Extensions tab via ##vso[task.uploadsummary].

Rendering is a pure function (render) so it can be unit-tested.
"""

import datetime
import json
import os
import re
import sys
import urllib.request

ICON = {
    "succeeded": "✅ Succeeded",
    "succeededWithIssues": "⚠️ With issues",
    "failed": "❌ Failed",
    "canceled": "⏹️ Canceled",
    "skipped": "⏭️ Skipped",
    "abandoned": "⏹️ Abandoned",
}
NOT_RUN = "⏳ Not run"
ORDER = ["failed", "canceled", "abandoned", "notrun",
         "succeededWithIssues", "skipped", "succeeded"]


def _ts(value):
    if not value:
        return None
    return datetime.datetime.fromisoformat(value.rstrip("Z").split(".")[0])


def duration(record):
    start, end = _ts(record.get("startTime")), _ts(record.get("finishTime"))
    if not start or not end:
        return ""
    m, s = divmod(int((end - start).total_seconds()), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m" if h else f"{m}m {s:02d}s"


def find_job(jobs, key):
    """Timeline job record of matrix leg *key* ("Build BSP <key>")."""
    for r in jobs:
        name, ident = r.get("name") or "", r.get("identifier") or ""
        if name == key or name.endswith(" " + key) or ident.endswith("." + key):
            return r
    return None


def _rank(result):
    return ORDER.index(result) if result in ORDER else 0


def render(matrix, records, check_only, deploy, pull_request, overrides=()):
    """Markdown summary for *matrix* ({key: {"BSP_NAME": ...}}) and timeline *records*.

    *overrides* are the repo override specs the run was built with.
    """
    lines = ["# BSP build summary", ""]
    if not matrix:
        lines.append("No presets were selected or matrix generation failed; "
                     "see the *Discover BSP Variants* job.")
        return "\n".join(lines) + "\n"

    jobs = [r for r in records if r.get("type") == "Job"]
    tasks = [r for r in records if r.get("type") == "Task"]

    rows, counts = [], {}
    for key, val in matrix.items():
        preset = val.get("BSP_NAME", key)
        rec = find_job(jobs, key) or {}
        result = rec.get("result") or "notrun"
        counts[result] = counts.get(result, 0) + 1
        dep = ""
        if deploy and rec:
            task = next((t for t in tasks if t.get("parentId") == rec.get("id")
                         and t.get("name") == "Deploy artifacts"), {})
            dep = ICON.get(task.get("result") or "", "—")
        logs = f"`failure-logs-{preset}-{rec.get('attempt', 1)}`" if result == "failed" else ""
        rows.append((_rank(result), preset, ICON.get(result, NOT_RUN), duration(rec), dep, logs))
    rows.sort()

    mode = "Check only (`bsp build --checkout`)" if check_only else "Full build"
    if pull_request:
        mode += ", pull request"
    totals = ", ".join(
        f"{n} {ICON.get(k, NOT_RUN).split(' ', 1)[1].lower()}"
        for k, n in sorted(counts.items(), key=lambda kv: _rank(kv[0])))
    lines += [f"**Mode:** {mode}  ",
              f"**Deploy:** {'on' if deploy else 'off'}  ",
              *([f"**Repo overrides:** {', '.join(f'`{o}`' for o in overrides)}  "]
                if overrides else []),
              f"**Presets:** {totals}",
              ""]

    head = ["Preset", "Result", "Duration"] + (["Deploy"] if deploy else []) + ["Failure logs artifact"]
    lines += ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for _, preset, res, dur, dep, logs in rows:
        cells = [f"`{preset}`", res, dur] + ([dep] if deploy else []) + [logs]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def fetch_timeline(env):
    url = (f"{env['SYSTEM_COLLECTIONURI']}{env['SYSTEM_TEAMPROJECT']}"
           f"/_apis/build/builds/{env['BUILD_BUILDID']}/timeline?api-version=7.1")
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {env.get('SYSTEM_ACCESSTOKEN', '')}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp).get("records") or []


def main():
    env = os.environ
    pull_request = env.get("BUILD_REASON") == "PullRequest"
    check_only = env.get("CHECK_ONLY") == "True" or pull_request
    deploy = env.get("DEPLOY") == "True" and not check_only

    try:
        matrix = json.loads(env.get("BSP_MATRIX") or "{}")
    except ValueError:
        matrix = {}

    records = []
    if matrix:
        try:
            records = fetch_timeline(env)
        except Exception as exc:  # summary must never fail the run
            print(f"##vso[task.logissue type=warning]Could not read run timeline: {exc}")

    overrides = [o for o in re.split(r"[\s,]+", env.get("REPO_OVERRIDES") or "") if o]
    text = render(matrix, records, check_only, deploy, pull_request, overrides)
    out = os.path.join(env.get("AGENT_TEMPDIRECTORY", "."), "bsp-summary.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"##vso[task.uploadsummary]{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
