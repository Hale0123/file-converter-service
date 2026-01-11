import sys
import os

# Make repo root importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from apps.worker.pipeline.sheet_svg import main

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/run_sheet.py <step_file>")
        sys.exit(1)

    step_path = sys.argv[1]
    main(step_path)
