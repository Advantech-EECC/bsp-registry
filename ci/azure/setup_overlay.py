#!/usr/bin/env python3
"""Register the CI overlay "ci" for azure-pipelines.yml.

usage: setup_overlay.py <sources-dir> <config-file>

Writes a bsp-registry-tools overlays config (BSP_OVERLAYS_CONFIG) holding one
overlay named "ci" and exports BSP_OVERLAYS_CONFIG to the following steps, so
every bsp command can run with "--overlay ci" without touching the agent
user's ~/.config/bsp/overlays.yaml.

When BSP_CACHE_ROOT is set (pipeline parameter "cacheRoot"), the overlay
merges ci/azure/overlay/registry.yaml, which moves DL_DIR/SSTATE_DIR below
that directory. Otherwise the overlay is empty and the registry's cache
paths are used.

The config is written as JSON, which is valid YAML, so no PyYAML is needed.
"""

import json
import os
import sys

OVERLAY_NAME = "ci"
OVERLAY_REGISTRY = os.path.join("ci", "azure", "overlay", "registry.yaml")


def cache_root(env):
    """Normalised BSP_CACHE_ROOT, or "" when unset/blank."""
    root = (env.get("BSP_CACHE_ROOT") or "").strip()
    return root.rstrip("/") or ("/" if root else "")


def overlay_config(sources_dir, env):
    """The overlays config document for *env*."""
    entry = {"name": OVERLAY_NAME, "description": "azure-pipelines.yml CI overlay", "repos": {}}
    if cache_root(env):
        # bsp-registry-tools does not resolve relative registry paths.
        entry["registry"] = os.path.abspath(os.path.join(sources_dir, OVERLAY_REGISTRY))
    return {"overlays": [entry]}


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    sources_dir, config_file = argv[1], argv[2]
    config = overlay_config(sources_dir, os.environ)
    os.makedirs(os.path.dirname(os.path.abspath(config_file)), exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    root = cache_root(os.environ)
    print(f"Overlay '{OVERLAY_NAME}' written to {config_file}")
    print(f"Cache root: {root or '(registry default)'}")
    print(f"##vso[task.setvariable variable=BSP_OVERLAYS_CONFIG]{os.path.abspath(config_file)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
