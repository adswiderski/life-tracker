from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router

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

app.include_router(router=auth_router, prefix="/api/v1/auth", tags=["auth"])

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