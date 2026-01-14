# STEP → Engineering Drawing Converter (HLR)

This project converts `.STEP / .STP` CAD models into engineering drawing previews using OpenCascade (via `cadquery-ocp).

It generates:
- Isometric view (visible + dashed hidden lines)
- Front / Top / Right orthographic views
- All views placed on a single drawing sheet
- Output as SVG

This is a real CAD kernel pipeline (Hidden Line Removal), not a mock or viewer.

---

## Tech Stack

- Python 3.11
- OpenCascade (via cadquery-ocp)
- Hidden Line Removal (HLR)
- SVG generation
- Bash + Python CLI
- Linux / WSL2

---

## Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/Hale0123/file-converter-service.git
cd file-converter-service

# 2. System requirements (Ubuntu / WSL)
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# 3. Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

# 4. Install dependencies
pip install cadquery-ocp vtk matplotlib pillow numpy

# 5. Make CLI executable
chmod +x convert

# 6. (Optional) Verify STEP file validity
# Must start with:
# ISO-10303-21;
head -n 2 tests/fixtures/your_file.step

# 7. Convert a single STEP file
./convert tests/fixtures/your_file.step

# 8. Convert all STEP files in tests/fixtures
./convert --all

#9 Run back-end
pip install python-multipart
pip install uvicorn fastapi
python -m uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload


