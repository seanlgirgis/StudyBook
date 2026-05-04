from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(content={"ok": True})


@app.get("/ping")
def ping() -> JSONResponse:
    return JSONResponse(content={"ok": True})
