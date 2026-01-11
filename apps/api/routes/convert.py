from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import uuid

router = APIRouter()

UPLOAD_DIR = Path("output/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/convert")
async def convert(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    suffix = Path(file.filename).suffix.lower()
    if suffix not in [".step", ".stp"]:
        return {"error": "Only .step or .stp files are supported"}

    out_path = UPLOAD_DIR / f"{job_id}{suffix}"

    with open(out_path, "wb") as f:
        f.write(await file.read())

    return {
        "job_id": job_id,
        "saved_as": str(out_path)
    }

