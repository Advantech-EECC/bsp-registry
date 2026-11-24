#!/usr/bin/env bash
#
# preflight.sh <build-root> <min-free-gb> <preset> <release>
#
# Fails fast, before hours of building, if this agent cannot build the preset:
#   - Docker must be usable by the agent user (kas-container needs it).
#   - Isar presets (isar-* / debian-* / ubuntu-* releases) need privileged
#     containers (kas-container --isar).
#   - The cache root $BSP_CACHE_ROOT (pipeline parameter "cacheRoot", used
#     by the CI overlay) must be an existing directory writable by the agent
#     user. Blank means the registry default, $HOME/data/cache.
#   - At least <min-free-gb> GB free on the filesystem of the build
#     directory and of the cache root. 0 skips the check.
# Also logs basic agent facts to make agent-specific failures easier to spot.

set -uo pipefail

ROOT="$1"
MIN_GB="$2"
PRESET="$3"
RELEASE="$4"
CACHE_ROOT="$(echo "${BSP_CACHE_ROOT:-}" | xargs)"
CACHE="${CACHE_ROOT:-${HOME}/data/cache}"
FAIL=0

error() {
  echo "##vso[task.logissue type=error]Pre-flight: $*"
  FAIL=1
}

echo "Agent:   ${AGENT_NAME:-$(hostname)} ($(uname -srm))"
echo "CPUs:    $(nproc)"
echo "Memory:  $(awk '/MemTotal/ {printf "%.0f GB", $2/1024/1024}' /proc/meminfo)"
echo "Preset:  $PRESET (release ${RELEASE:-?})"

# --- Docker --------------------------------------------------------------------
if ! command -v docker >/dev/null 2>&1; then
  error "docker is not installed on this agent (needed by kas-container)."
elif ! docker info >/dev/null 2>&1; then
  error "docker is installed but not usable by user '$(id -un)' (daemon down, or user not in the docker group)."
else
  echo "Docker:  $(docker version --format '{{.Server.Version}}' 2>/dev/null)"
  if [[ "$PRESET" == isar-* || "$RELEASE" =~ ^(debian|ubuntu)- ]]; then
    if docker run --rm --privileged alpine true >/dev/null 2>&1; then
      echo "Privileged containers: OK (needed for Isar)"
    else
      error "privileged containers do not work on this agent; Isar builds need 'docker run --privileged'."
    fi
  fi
fi

# --- Cache root ----------------------------------------------------------------
echo "Cache:   $CACHE${CACHE_ROOT:+ (cacheRoot)}"
if [ -n "$CACHE_ROOT" ]; then
  if [ ! -d "$CACHE_ROOT" ]; then
    error "cache root $CACHE_ROOT does not exist on this agent. Create it (owned by '$(id -un)') or queue with another 'cacheRoot'."
  elif ! PROBE=$(mktemp "$CACHE_ROOT/.preflight.XXXXXX" 2>/dev/null); then
    error "cache root $CACHE_ROOT is not writable by user '$(id -un)'."
  else
    rm -f "$PROBE"
  fi
fi

# --- Disk space ------------------------------------------------------------------
free_gb() {
  df -Pk "$1" 2>/dev/null | awk 'NR == 2 {printf "%d", $4 / 1024 / 1024}'
}

if [ "${MIN_GB:-0}" -gt 0 ] 2>/dev/null; then
  mkdir -p "$ROOT" 2>/dev/null || true
  CACHE_DIR="$CACHE"
  [ -d "$CACHE_DIR" ] || CACHE_DIR="$HOME"
  declare -A SEEN=()
  for DIR in "$ROOT" "$CACHE_DIR"; do
    FS=$(df -P "$DIR" 2>/dev/null | awk 'NR == 2 {print $6}')
    [ -n "$FS" ] || { error "cannot determine filesystem of $DIR"; continue; }
    [ -n "${SEEN[$FS]:-}" ] && continue
    SEEN[$FS]=1
    GB=$(free_gb "$DIR")
    echo "Disk:    ${GB} GB free on $FS (for $DIR), need ${MIN_GB} GB"
    if [ "${GB:-0}" -lt "$MIN_GB" ]; then
      error "only ${GB} GB free on $FS ($DIR); at least ${MIN_GB} GB required. Free space or lower 'minimum free disk space'."
    fi
  done
else
  echo "Disk:    check skipped (minimum 0 GB)"
fi

if [ "$FAIL" -ne 0 ]; then
  echo "Pre-flight check failed; not starting the build."
  exit 1
fi
echo "Pre-flight check passed."
