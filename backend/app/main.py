from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import boxes, items, search

app = FastAPI(title="Storage Box Inventory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boxes.router)
app.include_router(items.router)
app.include_router(search.router)


@app.get("/health")
def health():
    return {"status": "ok"}
