#!/usr/bin/env python3
"""Generate the Azure Pipelines build matrix for azure-pipelines.yml.

Lists the presets of the local registry with ``bsp --no-color --local list``,
applies the queue-time selection (group checkboxes, "All presets", regex and
release filter, passed in as environment variables) and prints the matrix as
the output variable ``matrix`` of the step named ``generator``.

The selection logic lives in pure functions so it can be unit-tested
(see ci/azure/tests/).
"""

import json
import os
import re
import subprocess
import sys

# Group checkbox env var -> regex matched against the preset name.
GROUPS = {
    "GROUP_POKY": r"^poky-",
    "GROUP_ISAR": r"^isar-",
    "GROUP_MODULAR": r"^modular-",
    "GROUP_ADVANTECH": r"^advantech-",
    "GROUP_MEDIATEK": r"^mediatek-",
    "GROUP_QUALCOMM": r"^(qcm|qcs)[0-9]|^monaco-",
    "GROUP_ROCKCHIP": r"^rock-",
    "GROUP_NVIDIA": r"^jetson-",
}

# Release checkboxes (env var REL_<NAME>); "isar" covers debian-*/ubuntu-*.
YOCTO_RELEASES = ["kirkstone", "mickledore", "nanbield", "scarthgap",
                  "styhead", "walnascar", "whinlatter", "wrynose", "master"]

ISAR_RELEASE_RE = r"^(debian|ubuntu)-"


class SelectionError(Exception):
    """Invalid or empty selection; the message is shown to the user."""


def parse_bsp_list(output):
    """Parse 'bsp list' output into an ordered {preset: release} dict.

    Lines look like:
      - name: Description (device: dev, release: rel, features: ...)
    """
    presets = {}
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        match = re.match(r"- ([^:]+):", line)
        if not match:
            continue
        name = match.group(1).strip()
        rel = re.search(r"\(device: [^,]*, release: ([^,)]+)", line)
        presets[name] = rel.group(1).strip() if rel else ""
    return presets


def is_true(value):
    return (value or "").strip().lower() == "true"


def release_matches(release, ticked):
    """True if *release* is covered by one of the *ticked* release names.

    A Yocto release matches exactly or as a suffix (ros2-humble-scarthgap
    counts as scarthgap); "isar" matches debian-*/ubuntu-* distros.
    """
    for r in ticked:
        if r == "isar":
            if re.match(ISAR_RELEASE_RE, release):
                return True
        elif release == r or release.endswith("-" + r):
            return True
    return False


def ungrouped(presets):
    return [p for p in presets if not any(re.search(rx, p) for rx in GROUPS.values())]


def uncovered_releases(presets):
    return [p for p, rel in presets.items()
            if not release_matches(rel, YOCTO_RELEASES + ["isar"])]


def select(presets, env):
    """Apply the queue-time selection in *env* to *presets* ({name: release}).

    Returns (selected_names, log_lines). Raises SelectionError.
    """
    log = []
    if is_true(env.get("BUILD_ALL")):
        selected = list(presets)
        log.append("Selection: all presets")
    else:
        patterns = [rx for var, rx in GROUPS.items() if is_true(env.get(var))]
        user_rx = (env.get("PRESET_REGEX") or "").strip()
        if user_rx:
            try:
                re.compile(user_rx)
            except re.error as err:
                raise SelectionError(f"Invalid preset regex {user_rx!r}: {err}")
            patterns.append(user_rx)
        log.append("Selection patterns: " + (", ".join(patterns) or "<none>"))
        selected = [p for p in presets if any(re.search(rx, p) for rx in patterns)]

    ticked = [r for r in YOCTO_RELEASES if is_true(env.get("REL_" + r.upper()))]
    if is_true(env.get("REL_ISAR")):
        ticked.append("isar")
    if ticked:
        before = len(selected)
        selected = [p for p in selected if release_matches(presets[p], ticked)]
        log.append(f"Release filter {', '.join(ticked)}: {len(selected)} of {before} presets kept")

    if not selected:
        raise SelectionError(
            "No presets selected: tick a group or 'All presets', or enter a regex that "
            "matches at least one preset (and check that the release filter does not "
            "exclude all of them).")
    return selected, log


def build_matrix(selected, presets):
    """Azure matrix: {job_suffix: {VAR: value}}; job suffix is alphanumeric."""
    return {
        re.sub(r"[^a-zA-Z0-9]", "_", p): {"BSP_NAME": p, "BSP_RELEASE": presets[p]}
        for p in selected
    }


def main():
    print("Listing available BSPs...")
    # --local must match the build job, otherwise the matrix would be
    # generated from the remote (main) registry instead of this checkout.
    try:
        result = subprocess.run(["bsp", "--no-color", "--local", "list"],
                                capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"##vso[task.logissue type=error]'bsp list' failed: {exc.stderr}")
        return 1

    presets = parse_bsp_list(result.stdout)
    print(f"Found {len(presets)} variants.")
    # An empty matrix would skip every build and still report success.
    if not presets:
        print("##vso[task.logissue type=error]No BSP presets found in 'bsp list' output:")
        print(result.stdout)
        return 1

    for p in ungrouped(presets):
        print(f"##vso[task.logissue type=warning]Preset '{p}' is not in any group checkbox")
    for p in uncovered_releases(presets):
        print(f"##vso[task.logissue type=warning]Preset '{p}' (release '{presets[p]}') "
              "is not covered by any release checkbox")

    try:
        selected, log = select(presets, os.environ)
    except SelectionError as exc:
        print(f"##vso[task.logissue type=error]{exc}")
        return 1
    print("\n".join(log))

    print(f"Building {len(selected)} of {len(presets)} presets:")
    for p in selected:
        print(f"  {p}")

    matrix = build_matrix(selected, presets)
    print(f"##vso[task.setvariable variable=matrix;isOutput=true]{json.dumps(matrix)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
