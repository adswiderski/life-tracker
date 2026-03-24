from typing import Any
from fastapi import APIRouter, status
from . import schemas

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserCreate) -> dict[str, Any]:
    """Register a new user"""
    # TODO: Hashowanie + zapis do bazy
    return {
        "id": 1,
        "email": user.email,
        "created_at": "2024-03-25T07:00:00"
    }

@router.post("/login", response_model=schemas.Token)
async def login(email: str, password: str) -> dict[str, Any]:
    """Login user"""
    # TODO: Walidacja + generowanie JWT
    return {
        "access_token": "mock-access-token",
        "token_type": "bearer"
    }

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user()-> dict[str, Any]:
    """Get current user info"""
    # TODO: Walidacja JWT
    return {
        "id": 1,
        "email": "mock@mock.com",
        "created_at": "2024-03-25T07:00:00"
    }