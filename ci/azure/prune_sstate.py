#!/usr/bin/env python3
"""Prune unused entries from the shared Yocto/Isar sstate caches on this agent.

    prune_sstate.py <registry-dir> <days>

The sstate directories are read from the registry (every environment
variable named SSTATE_DIR in bsp-registry*.y*ml, with $ENV{VAR} expanded), so
they stay in sync with bsp-registry.yml. Files not accessed for <days> days
are deleted, then empty directories. The download caches (DL_DIR) are never
touched: upstream source archives disappear, and the cache may be the only
copy.

Safety:
  - runs at most once per 20 hours per agent (stamp file next to the cache)
    and never concurrently (lock file), so most build jobs skip it instantly;
  - skips filesystems mounted with 'noatime', where access times are not
    updated and "unused for N days" cannot be determined ('relatime', the
    Linux default, updates atime at least daily and is fine);
  - never fails the job.
"""

import fcntl
import glob
import os
import re
import sys
import time

import yaml

STAMP_MAX_AGE = 20 * 3600


def sstate_dirs(registry_dir, environ=os.environ):
    """All SSTATE_DIR values in the registry files, $ENV{VAR} expanded."""
    found = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("name") == "SSTATE_DIR" and isinstance(node.get("value"), str):
                found.append(node["value"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for path in sorted(glob.glob(os.path.join(registry_dir, "bsp-registry*.y*ml"))):
        with open(path, encoding="utf-8") as f:
            walk(yaml.safe_load(f))

    expanded = []
    for value in found:
        value = re.sub(r"\$ENV\{(\w+)\}", lambda m: environ.get(m.group(1), ""), value)
        if value and value not in expanded:
            expanded.append(value)
    return expanded


def mount_options(path, mounts_file="/proc/mounts"):
    """Mount options of the filesystem containing *path* (longest mount point match)."""
    path = os.path.realpath(path)
    best, opts = "", ""
    try:
        with open(mounts_file, encoding="utf-8") as f:
            for line in f:
                fields = line.split()
                if len(fields) < 4:
                    continue
                mnt = fields[1].replace("\\040", " ")
                if (path == mnt or path.startswith(mnt.rstrip("/") + "/")) and len(mnt) >= len(best):
                    best, opts = mnt, fields[3]
    except OSError:
        pass
    return opts.split(",") if opts else []


def prune(directory, days, now=None):
    """Delete files under *directory* not accessed for *days*; return (files, bytes)."""
    now = now or time.time()
    cutoff = now - days * 86400
    files = size = 0
    for root, dirs, names in os.walk(directory, topdown=False):
        for name in names:
            path = os.path.join(root, name)
            try:
                st = os.lstat(path)
                if st.st_atime < cutoff:
                    os.unlink(path)
                    files += 1
                    size += st.st_size
            except OSError:
                pass
        if root != directory:
            try:
                os.rmdir(root)  # only succeeds if empty
            except OSError:
                pass
    return files, size


def main(argv):
    registry_dir, days = argv[1], int(argv[2])
    if days <= 0:
        print("sstate pruning disabled (0 days).")
        return 0

    configured = sstate_dirs(registry_dir)
    dirs = [d for d in configured if os.path.isdir(d)]
    if not dirs:
        print("No existing SSTATE_DIR found; nothing to prune.")
        return 0

    # Stamp/lock live next to the caches, derived from all configured dirs
    # so the location does not move when one cache does not exist yet.
    if len(configured) > 1:
        state_dir = os.path.commonpath(configured)
    else:
        state_dir = os.path.dirname(configured[0])
    os.makedirs(state_dir, exist_ok=True)
    stamp = os.path.join(state_dir, ".ci-sstate-prune.stamp")
    lock_path = os.path.join(state_dir, ".ci-sstate-prune.lock")

    try:
        age = time.time() - os.path.getmtime(stamp)
        if age < STAMP_MAX_AGE:
            print(f"sstate pruned {age / 3600:.1f} h ago on this agent; skipping.")
            return 0
    except OSError:
        pass

    with open(lock_path, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            print("Another job is pruning the sstate cache; skipping.")
            return 0

        for d in dirs:
            if "noatime" in mount_options(d):
                print(f"##vso[task.logissue type=warning]{d} is on a 'noatime' filesystem; "
                      "access times are not tracked, so it is not pruned.")
                continue
            start = time.time()
            files, size = prune(d, days)
            print(f"Pruned {d}: {files} files, {size / 1024 ** 3:.1f} GB not used for "
                  f"{days} days ({time.time() - start:.0f} s)")

        with open(stamp, "w") as f:
            f.write(time.strftime("%Y-%m-%dT%H:%M:%S\n"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as exc:  # pruning must never fail a build job
        print(f"##vso[task.logissue type=warning]sstate pruning failed: {exc}")
        sys.exit(0)
