#!/usr/bin/env bash
#
# collect_failure_logs.sh <build-dir> <output-dir>
#
# Copies what is needed to debug a failed BSP build out of <build-dir>
# (build/<preset>) into <output-dir>, before the build directory is deleted:
#   - README.txt with preset / run / commit (from PRESET, RUN_INFO, COMMIT_INFO)
#   - build-manifest.json and build/conf/
#   - bitbake cooker console log per machine (console-<machine>.log)
#   - the log of every failed task (failed-tasks/)
# Never fails.

SRC="$1"
OUT="$2"

rm -rf "$OUT"
mkdir -p "$OUT/failed-tasks"
{
  echo "Preset:  ${PRESET:-?}"
  echo "Run:     ${RUN_INFO:-?}"
  echo "Commit:  ${COMMIT_INFO:-?}"
} > "$OUT/README.txt"

if [ ! -d "$SRC" ]; then
  echo "Build directory $SRC does not exist (failed before kas ran)." >> "$OUT/README.txt"
  exit 0
fi

cp -L "$SRC/build-manifest.json" "$OUT/" 2>/dev/null || true
cp -rL "$SRC/build/conf" "$OUT/conf" 2>/dev/null || true

for LOG in "$SRC"/build/tmp*/log/cooker/*/console-latest.log; do
  [ -e "$LOG" ] || continue
  MACHINE_DIR="${LOG%/console-latest.log}"
  cp -L "$LOG" "$OUT/console-${MACHINE_DIR##*/}.log"
done

# Bitbake prints "Logfile of failure stored in: <path>" per failed task.
# Paths may be container paths (/build, /work) from kas-container.
grep -ho "Logfile of failure stored in: [^ ]*" "$OUT"/console-*.log 2>/dev/null |
  awk '{print $NF}' | sort -u | while read -r P; do
    for C in "$P" "$SRC/build/${P#/build/}" "$SRC/${P#/work/}"; do
      if [ -f "$C" ]; then
        # Keep <arch>/<recipe>/<version>/temp/log.do_<task>.<pid> as the name.
        NAME="${C##*/work/}"
        cp -L "$C" "$OUT/failed-tasks/${NAME//\//__}"
        break
      fi
    done
  done

echo "Collected:"
find "$OUT" -type f | sed "s|^$OUT/|  |"
exit 0
