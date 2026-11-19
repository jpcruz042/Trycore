from fastapi import FastAPI

app = FastAPI(
    title="Trycore EVM API",
    version="0.1.0",
    description="API para proyectos, actividades e indicadores EVM.",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return service availability for container monitoring."""
    return {"status": "ok"}
