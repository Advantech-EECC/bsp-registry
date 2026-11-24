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


class RepoOverridesTest(unittest.TestCase):
    def test_split_on_whitespace_and_commas(self):
        env = {"REPO_OVERRIDES": " meta-a@feat/x,meta-b=https://h/b.git@tag:v1\n meta-a@feat/x "}
        self.assertEqual(so.repo_overrides(env), ["meta-a@feat/x", "meta-b=https://h/b.git@tag:v1"])

    def test_blank(self):
        self.assertEqual(so.repo_overrides({"REPO_OVERRIDES": " "}), [])
        self.assertEqual(so.repo_overrides({}), [])


class MainTest(unittest.TestCase):
    def test_writes_config_and_exports_variable(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "sub", "overlays.yaml")
            buf = io.StringIO()
            with mock.patch.dict(os.environ, {"BSP_CACHE_ROOT": "/ssd", "REPO_OVERRIDES": ""}), \
                    redirect_stdout(buf):
                self.assertEqual(so.main(["x", "/src", out]), 0)
            with open(out) as f:
                self.assertEqual(json.load(f)["overlays"][0]["name"], "ci")
            self.assertIn(f"##vso[task.setvariable variable=BSP_OVERLAYS_CONFIG]{out}", buf.getvalue())

    def run_with_overrides(self, returncode):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "overlays.yaml")
            buf = io.StringIO()
            done = mock.Mock(returncode=returncode, stdout="", stderr="bad spec")
            with mock.patch.dict(os.environ, {"REPO_OVERRIDES": "meta-a@x meta-b@y"}), \
                    mock.patch.object(so.subprocess, "run", return_value=done) as run, \
                    redirect_stdout(buf):
                rc = so.main(["x", "/src", out])
            return rc, run, buf.getvalue(), out

    def test_overrides_added_with_bsp_set_repo(self):
        rc, run, text, out = self.run_with_overrides(0)
        self.assertEqual(rc, 0)
        first = run.call_args_list[0]
        self.assertEqual(first.args[0], ["bsp", "--no-color", "overlay", "set-repo", "ci", "meta-a@x"])
        self.assertEqual(first.kwargs["env"]["BSP_OVERLAYS_CONFIG"], out)
        self.assertEqual(run.call_args_list[1].args[0][-1], "meta-b@y")
        self.assertIn("Building with repo overrides: meta-a@x meta-b@y", text)

    def test_invalid_override_fails(self):
        rc, run, text, _ = self.run_with_overrides(1)
        self.assertEqual(rc, 1)
        self.assertEqual(run.call_count, 1)
        self.assertIn("Invalid repo override 'meta-a@x': bad spec", text)


if __name__ == "__main__":
    unittest.main()
