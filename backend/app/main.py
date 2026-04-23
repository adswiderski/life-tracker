from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.fitness.router import router as fitness_router
from app.auth.router import router as auth_router
from app.learning.router import router as learning_router

from app.core.config import settings

app = FastAPI(
    title="Life Tracker API",
    description="Plan life, play life",
    version="0.1.0",
)

# Póki co
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=auth_router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["auth"]
)
app.include_router(
    fitness_router, prefix=f"{settings.API_V1_PREFIX}/fitness", tags=["fitness"]
)
app.include_router(
    learning_router, prefix=f"{settings.API_V1_PREFIX}/learning", tags=["learning"]
)


@app.get("/")
def root():
    return {
        "message": app.title,
        "version": app.version,
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "c00l"}
