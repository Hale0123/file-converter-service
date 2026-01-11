import argparse
import os
import sys
from pathlib import Path

# Make repo root importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from apps.worker.pipeline.sheet_svg import main as make_sheet  # noqa: E402


def is_step_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in {".stp", ".step"}


def out_name_for(inp: Path) -> str:
    # e.g., tests/fixtures/part.step -> output/part_sheet.svg
    stem = inp.stem
    return f"output/{stem}_sheet.svg"


def convert_one(inp: Path) -> str:
    out_svg = out_name_for(inp)
    os.makedirs("output", exist_ok=True)
    make_sheet(str(inp), out_svg=out_svg)
    return out_svg


def main():
    ap = argparse.ArgumentParser(prog="convert", description="STEP -> multi-view sheet SVG")
    ap.add_argument("path", nargs="?", help="Path to .stp/.step file (omit if using --all)")
    ap.add_argument("--all", action="store_true", help="Convert all STEP files in tests/fixtures/")
    args = ap.parse_args()

    if args.all:
        fixtures = Path("tests/fixtures")
        if not fixtures.exists():
            raise SystemExit("tests/fixtures does not exist")

        files = sorted([p for p in fixtures.rglob("*") if is_step_file(p)])
        if not files:
            raise SystemExit("No .stp/.step files found in tests/fixtures")

        print(f"Found {len(files)} STEP files in tests/fixtures")
        for p in files:
            out_svg = convert_one(p)
            print(f"✅ {p} -> {out_svg}")
        return

    if not args.path:
        raise SystemExit("Provide a STEP file path, or use --all")

    inp = Path(args.path)
    if not is_step_file(inp):
        raise SystemExit(f"Not a STEP file: {inp}")

    out_svg = convert_one(inp)
    print(f"✅ {inp} -> {out_svg}")


if __name__ == "__main__":
    main()
