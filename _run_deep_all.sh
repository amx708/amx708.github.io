#!/usr/bin/env bash
# 串行切片跑全量深凿升级（单进程内顺序，缓存共享安全）
cd "$(dirname "$0")"
PY=/c/Users/Administrator/AppData/Local/Programs/Python/Python313/python.exe
for s in 0 200 400 600 800 1000 1200; do
  echo "===== SLICE start=$s end=$((s+200)) ====="
  "$PY" _build_deep_all.py --start "$s" --end $((s+200))
done
echo "===== ALL DONE ====="
