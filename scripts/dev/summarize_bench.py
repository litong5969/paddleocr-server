#!/usr/bin/env python3
import argparse, ast, re, sys
from pathlib import Path

def parse_lines(p: Path):
    rows = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                obj = ast.literal_eval(line)
                rows.append(obj)
            except Exception:
                pass
    return rows

def to_table(rows):
    out = []
    out.append("| concurrency | ok | err | p50 | p95 | p99 | avg |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in rows:
        out.append(f"| {r.get('concurrency')} | {r.get('ok')} | {r.get('err')} | {r.get('p50'):.4f} | {r.get('p95'):.4f} | {r.get('p99'):.4f} | {r.get('avg'):.4f} |")
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bench_file", help="bench markdown file path")
    args = ap.parse_args()
    rows = parse_lines(Path(args.bench_file))
    print(to_table(rows))

if __name__ == "__main__":
    main()

