#!/usr/bin/env bash
#
# install_trivy.sh <version> <bin-dir>
#
# Makes trivy available for 'bsp scan'. If trivy is already on PATH nothing
# is downloaded; otherwise the given release is downloaded from GitHub into
# <bin-dir>, verified against the release's checksums file, and <bin-dir> is
# prepended to PATH for the following pipeline steps.

set -euo pipefail

V="$1"
BIN="$2"

if command -v trivy >/dev/null 2>&1; then
  echo "Using trivy from PATH: $(command -v trivy)"
  trivy --version
  exit 0
fi

case "$(uname -m)" in
  x86_64)  A=64bit ;;
  aarch64) A=ARM64 ;;
  *) echo "##vso[task.logissue type=error]No Trivy build for $(uname -m)"; exit 1 ;;
esac

TGZ="trivy_${V}_Linux-${A}.tar.gz"
REL="https://github.com/aquasecurity/trivy/releases/download/v${V}"
mkdir -p "$BIN"
echo "Installing Trivy $V into $BIN"
(
  cd "$BIN"
  curl -sSfLO "$REL/$TGZ"
  curl -sSfLO "$REL/trivy_${V}_checksums.txt"
  grep " $TGZ\$" "trivy_${V}_checksums.txt" | sha256sum -c -
  tar -xzf "$TGZ" trivy
)
"$BIN/trivy" --version
echo "##vso[task.prependpath]$BIN"
