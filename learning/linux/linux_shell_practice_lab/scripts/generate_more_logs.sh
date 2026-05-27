#!/usr/bin/env bash
set -e

mkdir -p logs/generated

for day in 01 02 03; do
  out="logs/generated/app_2026_05_${day}.log"
  echo "Creating $out"
  cat > "$out" <<EOF
2026-05-${day} 09:00:00 INFO daily job started
2026-05-${day} 09:02:00 WARN slow response from dependency
2026-05-${day} 09:05:00 ERROR timeout while reading input
2026-05-${day} 09:10:00 INFO retry succeeded
2026-05-${day} 09:15:00 ERROR failed record count validation
EOF
done
