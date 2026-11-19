from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.activities import router as activities_router
from app.projects import router as projects_router

app = FastAPI(
    title="Trycore EVM API",
    version="0.1.0",
    description="API para proyectos, actividades e indicadores EVM.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)
app.include_router(activities_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return service availability for container monitoring."""
    return {"status": "ok"}
