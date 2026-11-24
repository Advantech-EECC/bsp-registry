"""Unit tests for ci/azure/setup_overlay.py."""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import setup_overlay as so  # noqa: E402


class OverlayConfigTest(unittest.TestCase):
    def test_cache_root_set_adds_absolute_registry(self):
        cfg = so.overlay_config("/src", {"BSP_CACHE_ROOT": "/build/ssd/azure/"})
        (entry,) = cfg["overlays"]
        self.assertEqual(entry["name"], "ci")
        self.assertEqual(entry["registry"], "/src/ci/azure/overlay/registry.yaml")
        self.assertEqual(entry["repos"], {})

    def test_blank_cache_root_means_registry_default(self):
        for env in ({}, {"BSP_CACHE_ROOT": " "}):
            self.assertNotIn("registry", so.overlay_config("/src", env)["overlays"][0])

    def test_cache_root_normalised(self):
        self.assertEqual(so.cache_root({"BSP_CACHE_ROOT": " /a/b// "}), "/a/b")
        self.assertEqual(so.cache_root({"BSP_CACHE_ROOT": "/"}), "/")

    def test_overlay_registry_file_exists(self):
        root = os.path.join(os.path.dirname(__file__), "..", "..", "..")
        self.assertTrue(os.path.isfile(os.path.join(root, so.OVERLAY_REGISTRY)))


class MainTest(unittest.TestCase):
    def test_writes_config_and_exports_variable(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "sub", "overlays.yaml")
            buf = io.StringIO()
            with mock.patch.dict(os.environ, {"BSP_CACHE_ROOT": "/ssd"}), redirect_stdout(buf):
                self.assertEqual(so.main(["x", "/src", out]), 0)
            with open(out) as f:
                self.assertEqual(json.load(f)["overlays"][0]["name"], "ci")
            self.assertIn(f"##vso[task.setvariable variable=BSP_OVERLAYS_CONFIG]{out}", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
