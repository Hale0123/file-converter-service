from fastapi import FastAPI
from apps.api.routes.convert import router as convert_router

app = FastAPI(title="STEP2Drawing Service")

app.include_router(convert_router)

@app.get("/health")
def health():
    return {"status": "ok"}
