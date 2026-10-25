#!/usr/bin/env python3
"""Verify that the Markdown documentation matches the BSP registry and the file tree.

The registry is the single source of truth. Documentation drifts silently whenever a
preset is renamed, a patch is added or a directory is restructured, so this script
re-derives the facts from ``bsp-registry.yml`` (plus any file pulled in through its
top-level ``include:`` directive) and the working tree, and compares them against what
the Markdown files claim.

Checks performed:

1. ``bsp <verb> <name>`` command examples in fenced code blocks reference a real preset.
2. Repository-relative file paths referenced from Markdown actually exist.
3. The patch count stated in ``README.md`` matches the number of ``*.patch`` files.
4. Every file under ``patches/`` is mentioned in ``patches/README.md``.
5. The ``include:`` list of ``bsp-registry.yml`` and the README "Registry File Layout"
   table agree in both directions.
6. Backticked preset-looking names inside Markdown table cells exist in the registry.
7. Tables carrying both a "Preset" and a "(Supported) Releases" column state exactly
   the releases the registry defines for those presets.
8. Every preset in the registry is mentioned in at least one Markdown file.

Exits non-zero when any check fails so it can be wired into CI.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_FILE = "bsp-registry.yml"

# Markdown files are scanned recursively; these directories never contain docs we own.
SKIPPED_DIRS = {".git", "venv", ".venv", "build", "layers", "node_modules", "__pycache__"}

# Fenced code blocks are the only place we look for ``bsp`` invocations, so that prose
# mentioning a command in passing does not trip the checker.
FENCE_RE = re.compile(r"^\s*```")
BSP_COMMAND_RE = re.compile(
    r"\bbsp\s+(?:--[\w-]+\s+)*(?P<verb>build|shell|export|flash|deploy|lava|show)\s+"
    r"(?P<name>[A-Za-z0-9][\w.-]*)"
)
# Inline-code paths such as `vendors/nvidia/README.md` or `isar/distro/debian-trixie.yaml`.
INLINE_PATH_RE = re.compile(r"`([A-Za-z0-9_][\w./-]*\.(?:ya?ml|md|patch|sh|py|bb|bbappend))`")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)\s]*)?\)")
PATCH_COUNT_RE = re.compile(r"\*\*(\d+)\s+patches\*\*")

# Placeholders and generic examples that intentionally do not name a real preset.
PLACEHOLDER_NAMES = {
    "bsp_name",
    "bsp-name",
    "name",
}

# Names used in "how to add your own board" examples, which deliberately do not exist.
PLACEHOLDER_PREFIXES = ("my-board", "my-vendor")

# References that legitimately do not resolve inside this repository: files produced by
# a build, files living in upstream layers the patches apply to, and naming templates.
EXTERNAL_REFERENCES = {
    "final.yaml",
    "imx-setup-release.sh",
    "kas-configuration.yaml",
    "kas-configuration-file.yaml",
    "NNNN-Brief-description.patch",
    "conf/layer.conf",
    "classes/image_types_ostree.bbclass",
    "classes/image_types_ota.bbclass",
    "lib/oeqa/selftest/cases/updater_qemux86_64.py",
    "recipes-sota/aktualizr/aktualizr_git.bb",
    "imx-image-%.bbappend",
}

# Preset-looking names that tables may mention even though the registry does not (yet)
# define them, e.g. boards that are announced as planned. Extend this list for new
# intentional exceptions instead of loosening the table checks.
PLANNED_PRESET_NAMES: set[str] = set()

# Backticked tokens inside table cells; candidates for the preset-existence check.
TABLE_CODE_RE = re.compile(r"`([A-Za-z0-9][A-Za-z0-9._/-]*)`")


def load_registry(root: str) -> dict:
    """Load the registry, merging every file referenced by the top-level ``include:``."""
    with open(os.path.join(root, REGISTRY_FILE), encoding="utf-8") as handle:
        registry = yaml.safe_load(handle)

    merged = dict(registry)
    for included in registry.get("include") or []:
        with open(os.path.join(root, included), encoding="utf-8") as handle:
            extra = yaml.safe_load(handle) or {}
        for key, value in (extra.get("registry") or {}).items():
            # The registry merges list-valued sections by concatenation.
            merged.setdefault("registry", {}).setdefault(key, [])
            merged["registry"][key] = list(merged["registry"][key]) + list(value)
    return merged


def preset_names(registry: dict) -> set[str]:
    """Expand registry presets into the names accepted by the ``bsp`` CLI.

    A preset carrying ``releases:`` yields one name per release (``<name>-<release>``);
    a preset carrying a single ``release:`` is addressed by its bare name.
    """
    names: set[str] = set()
    for preset in registry.get("registry", {}).get("bsp") or []:
        name = preset.get("name")
        if not name:
            continue
        releases = preset.get("releases")
        if releases:
            names.update(f"{name}-{release}" for release in releases)
        else:
            names.add(name)
    return names


def preset_releases(registry: dict) -> dict[str, list[str]]:
    """Map each preset base name to the list of releases the registry defines for it.

    A preset carrying a single ``release:`` maps to a one-element list; a preset
    without any release information maps to an empty list.
    """
    releases: dict[str, list[str]] = {}
    for preset in registry.get("registry", {}).get("bsp") or []:
        name = preset.get("name")
        if not name:
            continue
        if preset.get("releases"):
            releases[name] = list(preset["releases"])
        elif preset.get("release"):
            releases[name] = [preset["release"]]
        else:
            releases[name] = []
    return releases


def markdown_files(root: str) -> list[str]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIPPED_DIRS]
        for filename in filenames:
            if filename.endswith(".md"):
                found.append(os.path.join(dirpath, filename))
    return sorted(found)


def code_block_lines(text: str) -> list[str]:
    """Return only the lines that live inside fenced code blocks."""
    inside = False
    lines = []
    for line in text.splitlines():
        if FENCE_RE.match(line):
            inside = not inside
            continue
        if inside:
            lines.append(line)
    return lines


def check_preset_references(root: str, docs: list[str], presets: set[str]) -> list[str]:
    errors = []
    for path in docs:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        relative = os.path.relpath(path, root)
        for line in code_block_lines(text):
            for match in BSP_COMMAND_RE.finditer(line):
                name = match.group("name")
                if name.startswith("<") or name in PLACEHOLDER_NAMES:
                    continue
                if name.startswith(PLACEHOLDER_PREFIXES):
                    continue
                if name not in presets:
                    errors.append(
                        f"{relative}: 'bsp {match.group('verb')} {name}' "
                        f"references a preset that is not in the registry"
                    )
    return errors


def check_referenced_paths(root: str, docs: list[str]) -> list[str]:
    errors = []
    for path in docs:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        relative = os.path.relpath(path, root)
        doc_dir = os.path.dirname(path)

        candidates: set[tuple[str, str]] = set()
        for match in INLINE_PATH_RE.finditer(text):
            # Skip inline code that is the label of a Markdown link, e.g. [`a.yml`](dir/a.yml).
            # The link target is checked separately and carries the resolvable path.
            if text[match.end():match.end() + 2] == "](":
                continue
            candidates.add((match.group(1), "inline reference"))
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1)
            if "://" in target or target.startswith("mailto:"):
                continue
            candidates.add((target, "link"))

        for target, kind in sorted(candidates):
            if target in EXTERNAL_REFERENCES:
                continue
            # Try the path relative to the document first, then relative to the repo root,
            # since docs use both conventions.
            if os.path.exists(os.path.join(doc_dir, target)):
                continue
            if os.path.exists(os.path.join(root, target)):
                continue
            errors.append(f"{relative}: {kind} '{target}' does not exist")
    return errors


def collect_patches(root: str) -> list[str]:
    patches_dir = os.path.join(root, "patches")
    found = []
    for dirpath, _dirnames, filenames in os.walk(patches_dir):
        for filename in filenames:
            if filename.endswith(".patch"):
                found.append(
                    os.path.relpath(os.path.join(dirpath, filename), root)
                )
    return sorted(found)


def check_patch_count(root: str, patches: list[str]) -> list[str]:
    readme = os.path.join(root, "README.md")
    with open(readme, encoding="utf-8") as handle:
        text = handle.read()
    match = PATCH_COUNT_RE.search(text)
    if not match:
        return ["README.md: no '**N patches**' statement found in the Patches section"]
    stated = int(match.group(1))
    if stated != len(patches):
        return [
            f"README.md: states '{stated} patches' but the tree contains {len(patches)}"
        ]
    return []


def check_patches_documented(root: str, patches: list[str]) -> list[str]:
    readme = os.path.join(root, "patches", "README.md")
    with open(readme, encoding="utf-8") as handle:
        text = handle.read()
    errors = []
    for patch in patches:
        # Match on the path relative to patches/, not just the basename: several releases
        # carry patches with identical filenames, and matching on the basename alone would
        # let a dropped patch hide behind its namesake.
        relative = os.path.relpath(patch, "patches")
        if relative not in text:
            errors.append(f"patches/README.md: '{patch}' is not documented")
    return errors


def check_include_list_documented(root: str, registry: dict) -> list[str]:
    """The README Registry File Layout table and the root ``include:`` list must agree."""
    includes = set(registry.get("include") or [])
    readme = os.path.join(root, "README.md")
    with open(readme, encoding="utf-8") as handle:
        text = handle.read()

    documented = set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        for token in TABLE_CODE_RE.findall(line):
            if re.fullmatch(r"bsp-registry\.[\w-]+\.ya?ml", token):
                documented.add(token)

    errors = []
    for missing in sorted(includes - documented):
        errors.append(
            f"README.md: included registry fragment '{missing}' is missing from the "
            f"Registry File Layout table"
        )
    for stale in sorted(documented - includes):
        errors.append(
            f"README.md: Registry File Layout table lists '{stale}', which is not in "
            f"the include: list of {REGISTRY_FILE}"
        )
    return errors


def non_preset_entities(registry: dict) -> set[str]:
    """Names the registry defines that are not presets but may appear in table cells:
    vendor slugs, distro slugs, container names and build-environment names."""
    names: set[str] = set()
    for vendor in registry.get("registry", {}).get("vendors") or []:
        if vendor.get("slug"):
            names.add(vendor["slug"])
    for distro in registry.get("registry", {}).get("distro") or []:
        if distro.get("slug"):
            names.add(distro["slug"])
    for container in registry.get("containers") or []:
        names.update(container.keys())
    names.update((registry.get("environments") or {}).keys())
    return names


def check_table_preset_names(
    root: str, docs: list[str], bases: dict[str, list[str]], presets: set[str], registry: dict
) -> list[str]:
    """Backticked preset-looking names in table cells must exist in the registry.

    A token "looks like a preset" when its first hyphen-separated segment matches the
    first segment of a real preset name; this keeps device names, feature names and
    file names out of the check without hardcoding every table.
    """
    prefixes = {name.split("-", 1)[0] for name in bases}
    known = set(bases) | presets | non_preset_entities(registry)
    errors = []
    for path in docs:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        relative = os.path.relpath(path, root)
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.lstrip().startswith("|"):
                continue
            for token in TABLE_CODE_RE.findall(line):
                if "/" in token or "." in token or "-" not in token:
                    continue
                if token.split("-", 1)[0] not in prefixes:
                    continue
                if token in known or token in PLANNED_PRESET_NAMES:
                    continue
                errors.append(
                    f"{relative}:{number}: table mentions preset '{token}', "
                    f"which is not in the registry"
                )
    return errors


def check_table_release_lists(
    root: str, docs: list[str], bases: dict[str, list[str]]
) -> list[str]:
    """Tables with "Preset" and "(Supported) Releases" columns must match the registry."""
    errors = []
    for path in docs:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
        relative = os.path.relpath(path, root)

        preset_col = releases_col = None
        for number, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped.startswith("|"):
                preset_col = releases_col = None
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            headers = [cell.strip("*` ").lower() for cell in cells]
            if "preset" in headers and (
                "supported releases" in headers or "releases" in headers
            ):
                preset_col = headers.index("preset")
                if "supported releases" in headers:
                    releases_col = headers.index("supported releases")
                else:
                    releases_col = headers.index("releases")
                continue
            if preset_col is None or set(cells[0]) <= {"-", ":", " "}:
                continue
            if len(cells) <= max(preset_col, releases_col):
                continue

            row_presets = [
                token
                for token in TABLE_CODE_RE.findall(cells[preset_col])
                if token in bases
            ]
            if not row_presets:
                continue  # planned boards and placeholder rows carry no real preset
            expected = set()
            for name in row_presets:
                expected.update(bases[name])
            stated = {
                entry.strip().strip("`")
                for entry in cells[releases_col].split(",")
                if entry.strip().strip("`")
            }
            if stated != expected:
                errors.append(
                    f"{relative}:{number}: releases for {', '.join(row_presets)} are "
                    f"'{', '.join(sorted(stated))}' but the registry defines "
                    f"'{', '.join(sorted(expected))}'"
                )
    return errors


def check_presets_documented(root: str, docs: list[str], bases: dict[str, list[str]]) -> list[str]:
    """Every preset defined in the registry must be mentioned somewhere in the docs."""
    corpus = []
    for path in docs:
        with open(path, encoding="utf-8") as handle:
            corpus.append(handle.read())
    text = "\n".join(corpus)
    return [
        f"registry preset '{name}' is not mentioned in any Markdown file"
        for name in sorted(bases)
        if name not in text
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=REPO_ROOT,
        help="repository root to check (defaults to the repository containing this script)",
    )
    args = parser.parse_args()
    root = os.path.abspath(args.root)

    registry = load_registry(root)
    presets = preset_names(registry)
    bases = preset_releases(registry)
    docs = markdown_files(root)
    patches = collect_patches(root)

    errors: list[str] = []
    errors += check_preset_references(root, docs, presets)
    errors += check_referenced_paths(root, docs)
    errors += check_patch_count(root, patches)
    errors += check_patches_documented(root, patches)
    errors += check_include_list_documented(root, registry)
    errors += check_table_preset_names(root, docs, bases, presets, registry)
    errors += check_table_release_lists(root, docs, bases)
    errors += check_presets_documented(root, docs, bases)

    print(
        f"Checked {len(docs)} Markdown file(s) against "
        f"{len(presets)} preset(s) and {len(patches)} patch(es)."
    )
    if errors:
        print(f"\n{len(errors)} documentation inconsistency(ies) found:\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Documentation is consistent with the registry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
