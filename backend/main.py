from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import auth, agents, experiments
from backend.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PerplexiPlay API",
    description="Agent Playground and Testing Environment",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(experiments.router, prefix="/experiments", tags=["experiments"])


@app.get("/")
async def root():
    return {
        "message": "PerplexiPlay API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
