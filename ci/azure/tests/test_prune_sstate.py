"""Unit tests for ci/azure/prune_sstate.py."""

import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import prune_sstate as ps  # noqa: E402

REGISTRY_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")


class SstateDirsTest(unittest.TestCase):
    def test_reads_and_expands_registry(self):
        dirs = ps.sstate_dirs(REGISTRY_ROOT, {"HOME": "/home/agent"})
        self.assertIn("/home/agent/data/cache/sstate", dirs)
        self.assertIn("/home/agent/data/cache/isar/sstate", dirs)
        self.assertTrue(all("$ENV" not in d for d in dirs))

    def test_cache_root_uses_ci_overlay(self):
        dirs = ps.sstate_dirs(REGISTRY_ROOT, {"HOME": "/h", "BSP_CACHE_ROOT": " /ssd/azure/ "})
        self.assertEqual(sorted(dirs), ["/ssd/azure/isar/sstate", "/ssd/azure/sstate"])

    def test_blank_cache_root_uses_registry(self):
        dirs = ps.sstate_dirs(REGISTRY_ROOT, {"HOME": "/h", "BSP_CACHE_ROOT": " "})
        self.assertIn("/h/data/cache/sstate", dirs)

    def test_ignores_dl_dir(self):
        dirs = ps.sstate_dirs(REGISTRY_ROOT, {"HOME": "/h"})
        self.assertFalse(any("downloads" in d for d in dirs))


class MountOptionsTest(unittest.TestCase):
    def test_longest_mount_point_wins(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("/dev/a / ext4 rw,relatime 0 0\n/dev/b /data ext4 rw,noatime 0 0\n")
        try:
            self.assertIn("noatime", ps.mount_options("/data/cache/sstate", f.name))
            self.assertIn("relatime", ps.mount_options("/home/x", f.name))
            self.assertNotIn("noatime", ps.mount_options("/database", f.name))
        finally:
            os.unlink(f.name)


class PruneTest(unittest.TestCase):
    def test_deletes_only_old_files_and_empty_dirs(self):
        now = time.time()
        with tempfile.TemporaryDirectory() as d:
            old = os.path.join(d, "ab", "old.tar.zst")
            new = os.path.join(d, "cd", "new.tar.zst")
            for p in (old, new):
                os.makedirs(os.path.dirname(p))
                with open(p, "w") as f:
                    f.write("x" * 10)
            os.utime(old, (now - 40 * 86400, now - 40 * 86400))
            os.utime(new, (now - 5 * 86400, now - 50 * 86400))  # recently read, old mtime

            files, size = ps.prune(d, 30, now)

            self.assertEqual((files, size), (1, 10))
            self.assertFalse(os.path.exists(old))
            self.assertFalse(os.path.exists(os.path.dirname(old)))  # emptied dir removed
            self.assertTrue(os.path.exists(new))
            self.assertTrue(os.path.isdir(d))  # root kept


class MainTest(unittest.TestCase):
    def test_runs_once_then_skips(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as reg:
            sstate = os.path.join(home, "cache", "sstate")
            os.makedirs(sstate)
            with open(os.path.join(reg, "bsp-registry.yml"), "w") as f:
                f.write('environment:\n  variables:\n'
                        '    - name: "SSTATE_DIR"\n      value: "$ENV{TESTHOME}/cache/sstate"\n')
            os.environ["TESTHOME"] = home
            saved_root = os.environ.pop("BSP_CACHE_ROOT", None)
            try:
                self.assertEqual(ps.main(["x", reg, "30"]), 0)
                stamp = os.path.join(home, "cache", ".ci-sstate-prune.stamp")
                self.assertTrue(os.path.exists(stamp))
                mtime = os.path.getmtime(stamp)
                self.assertEqual(ps.main(["x", reg, "30"]), 0)
                self.assertEqual(os.path.getmtime(stamp), mtime)  # second run skipped
                self.assertEqual(ps.main(["x", reg, "0"]), 0)
            finally:
                del os.environ["TESTHOME"]
                if saved_root is not None:
                    os.environ["BSP_CACHE_ROOT"] = saved_root


if __name__ == "__main__":
    unittest.main()
