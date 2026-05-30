from fastapi import FastAPI
from routers import categories, todos
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List API",
    description="FastAPI + SQLAlchemy 2.0 + Pydantic v2 + SQLite + Uvicorn 프로젝트",
    version="1.0.0"
)

app.include_router(categories.router)
app.include_router(todos.router)

@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}

