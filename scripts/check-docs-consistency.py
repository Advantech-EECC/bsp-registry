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
    r"\bbsp\s+(?:--[\w-]+\s+)*(?P<verb>build|shell|export|flash|deploy|lava)\s+"
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
    "imx8mpevk",
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
        if os.path.basename(patch) not in text:
            errors.append(f"patches/README.md: '{patch}' is not documented")
    return errors


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
    docs = markdown_files(root)
    patches = collect_patches(root)

    errors: list[str] = []
    errors += check_preset_references(root, docs, presets)
    errors += check_referenced_paths(root, docs)
    errors += check_patch_count(root, patches)
    errors += check_patches_documented(root, patches)

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
