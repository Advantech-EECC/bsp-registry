"""Consistency checks between bsp-registry*.yml and the CI overlay.

The CI overlay (ci/azure/overlay/registry.yaml) moves DL_DIR/SSTATE_DIR of CI
builds below $BSP_CACHE_ROOT. It only works if it redefines every place the
registry defines them, otherwise builds using that environment silently fall
back to the registry paths ($HOME/data/cache).
"""

import glob
import os
import unittest

import yaml

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
OVERLAY = os.path.join(ROOT, "ci", "azure", "overlay", "registry.yaml")
CACHE_VARS = ("DL_DIR", "SSTATE_DIR")


def cache_var_definitions(doc, path=()):
    """{(scope..., var): value} for every DL_DIR/SSTATE_DIR in *doc*."""
    found = {}
    if isinstance(doc, dict):
        if doc.get("name") in CACHE_VARS and "value" in doc:
            found[path + (doc["name"],)] = doc["value"]
        for key, value in doc.items():
            found.update(cache_var_definitions(value, path + (str(key),)))
    elif isinstance(doc, list):
        for item in doc:
            found.update(cache_var_definitions(item, path))
    return found


def scope(key):
    """Registry scope of a definition: ("environment",) or ("environments", NAME)."""
    return key[:-2]  # drop "variables" and the variable name


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class OverlayCoverageTest(unittest.TestCase):
    def setUp(self):
        self.registry = {}
        for path in sorted(glob.glob(os.path.join(ROOT, "bsp-registry*.y*ml"))):
            for key, value in cache_var_definitions(load(path)).items():
                self.registry[key] = (os.path.basename(path), value)
        self.overlay = cache_var_definitions(load(OVERLAY))

    def test_registry_defines_cache_vars(self):
        self.assertIn(("environment", "variables", "SSTATE_DIR"), self.registry)

    def test_registry_defines_cache_vars_only_where_overlay_can_override(self):
        for key, (path, _) in self.registry.items():
            self.assertTrue(
                key[:1] == ("environment",) or (key[:1] == ("environments",) and len(key) == 4),
                f"{path} defines {key[-1]} at {'/'.join(key[:-1])}; the CI overlay can only "
                "override the global 'environment' and named 'environments'.")

    def test_overlay_redefines_every_registry_definition(self):
        for key, (path, _) in self.registry.items():
            self.assertIn(
                key, self.overlay,
                f"{path} sets {key[-1]} in {'/'.join(scope(key))}; add it to "
                "ci/azure/overlay/registry.yaml or CI builds of that environment ignore cacheRoot.")

    def test_overlay_values_are_below_cache_root(self):
        self.assertTrue(self.overlay)
        for key, value in self.overlay.items():
            self.assertTrue(value.startswith("$ENV{BSP_CACHE_ROOT}/"), f"{key}: {value}")

    def test_overlay_only_overrides_existing_environments(self):
        names = {k[1] for k in self.registry if k[0] == "environments"}
        for key in self.overlay:
            if key[0] == "environments":
                self.assertIn(key[1], names, f"overlay environment '{key[1]}' is not in the registry")

    def test_overlay_paths_are_distinct(self):
        values = list(self.overlay.values())
        self.assertEqual(len(values), len(set(values)))


if __name__ == "__main__":
    unittest.main()
