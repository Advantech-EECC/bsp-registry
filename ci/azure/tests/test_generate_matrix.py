"""Unit tests for ci/azure/generate_matrix.py (preset selection)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import generate_matrix as gm  # noqa: E402

LIST_OUTPUT = """\
Available BSP presets:
- poky-qemux86-64-scarthgap: Poky QEMU x86-64 (device: qemux86-64, release: scarthgap, features: systemd)
- poky-harden-qemux86-64-scarthgap: Hardened (device: qemux86-64, release: scarthgap, features: security)
- poky-qemux86-64-ros2-ros2-humble-scarthgap: ROS (device: qemux86-64, release: ros2-humble-scarthgap)
- isar-qemuamd64-debian-trixie: Isar (device: qemuamd64, release: debian-trixie)
- modular-bsp-rsb3720-wrynose: RSB3720 (device: rsb3720, release: wrynose, features: systemd)
- modular-bsp-rsb3720-walnascar: RSB3720 (device: rsb3720, release: walnascar)
- qcs6490-rb3gen2-core-kit-scarthgap: QCS6490 (device: qcs6490-rb3gen2-core-kit, release: scarthgap)
- monaco-monza-scarthgap: Monaco (device: monaco-monza, release: scarthgap)
- jetson-orin-nano-devkit-wrynose: Jetson (device: jetson-orin-nano-devkit, release: wrynose)
"""


class ParseTest(unittest.TestCase):
    def test_parse_names_and_releases(self):
        presets = gm.parse_bsp_list(LIST_OUTPUT)
        self.assertEqual(len(presets), 9)
        self.assertEqual(presets["modular-bsp-rsb3720-wrynose"], "wrynose")
        self.assertEqual(presets["isar-qemuamd64-debian-trixie"], "debian-trixie")

    def test_parse_ignores_other_lines(self):
        self.assertEqual(gm.parse_bsp_list("Available BSP presets:\n\nfoo\n"), {})

    def test_missing_release_is_empty(self):
        self.assertEqual(gm.parse_bsp_list("- foo: no details\n"), {"foo": ""})


class SelectTest(unittest.TestCase):
    def setUp(self):
        self.presets = gm.parse_bsp_list(LIST_OUTPUT)

    def sel(self, **env):
        return gm.select(self.presets, env)[0]

    def test_nothing_selected_raises(self):
        with self.assertRaises(gm.SelectionError):
            self.sel()

    def test_blank_regex_is_ignored(self):
        with self.assertRaises(gm.SelectionError):
            self.sel(PRESET_REGEX=" ")

    def test_invalid_regex_raises(self):
        with self.assertRaisesRegex(gm.SelectionError, "Invalid preset regex"):
            self.sel(PRESET_REGEX="([")

    def test_all(self):
        self.assertEqual(len(self.sel(BUILD_ALL="True")), 9)

    def test_group(self):
        self.assertEqual(self.sel(GROUP_MODULAR="True"),
                         ["modular-bsp-rsb3720-wrynose", "modular-bsp-rsb3720-walnascar"])

    def test_qualcomm_group_includes_monaco(self):
        self.assertEqual(self.sel(GROUP_QUALCOMM="True"),
                         ["qcs6490-rb3gen2-core-kit-scarthgap", "monaco-monza-scarthgap"])

    def test_groups_and_regex_are_a_union(self):
        self.assertEqual(self.sel(GROUP_NVIDIA="True", PRESET_REGEX="^isar-"),
                         ["isar-qemuamd64-debian-trixie", "jetson-orin-nano-devkit-wrynose"])

    def test_release_filter_narrows(self):
        self.assertEqual(self.sel(GROUP_MODULAR="True", REL_WRYNOSE="True"),
                         ["modular-bsp-rsb3720-wrynose"])

    def test_release_suffix_matches_ros2(self):
        got = self.sel(GROUP_POKY="True", REL_SCARTHGAP="True")
        self.assertIn("poky-qemux86-64-ros2-ros2-humble-scarthgap", got)
        self.assertEqual(len(got), 3)

    def test_isar_release_filter(self):
        self.assertEqual(self.sel(BUILD_ALL="True", REL_ISAR="True"),
                         ["isar-qemuamd64-debian-trixie"])

    def test_release_filter_leaving_nothing_raises(self):
        with self.assertRaises(gm.SelectionError):
            self.sel(GROUP_NVIDIA="True", REL_KIRKSTONE="True")

    def test_checkbox_values_are_case_insensitive(self):
        self.assertEqual(len(self.sel(BUILD_ALL="true")), 9)
        with self.assertRaises(gm.SelectionError):
            self.sel(BUILD_ALL="False")


class MatrixTest(unittest.TestCase):
    def test_matrix_keys_are_alphanumeric_and_unique(self):
        presets = gm.parse_bsp_list(LIST_OUTPUT)
        matrix = gm.build_matrix(list(presets), presets)
        self.assertEqual(len(matrix), len(presets))
        for key, val in matrix.items():
            self.assertRegex(key, r"^[A-Za-z0-9_]+$")
            self.assertEqual(val["BSP_RELEASE"], presets[val["BSP_NAME"]])

    def test_coverage_helpers(self):
        presets = {"foo-bar": "zeus", "poky-x": "scarthgap"}
        self.assertEqual(gm.ungrouped(presets), ["foo-bar"])
        self.assertEqual(gm.uncovered_releases(presets), ["foo-bar"])


class RegistryCoverageTest(unittest.TestCase):
    """Every preset in the real registry must be reachable via a group and a release checkbox.

    Runs only when 'bsp' is installed (skipped otherwise).
    """

    def test_registry_presets_are_covered(self):
        import shutil
        import subprocess
        if not shutil.which("bsp"):
            self.skipTest("bsp-registry-tools not installed")
        root = os.path.join(os.path.dirname(__file__), "..", "..", "..")
        out = subprocess.run(["bsp", "--no-color", "--local", "list"], cwd=root,
                             capture_output=True, text=True, check=True).stdout
        presets = gm.parse_bsp_list(out)
        self.assertTrue(presets)
        self.assertEqual(gm.ungrouped(presets), [], "add a group checkbox for these presets")
        self.assertEqual(gm.uncovered_releases(presets), [], "add a release checkbox for these")


if __name__ == "__main__":
    unittest.main()
