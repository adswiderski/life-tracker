from fastapi import APIRouter, HTTPException, status

from app.auth import schemas, service
from app.core.security import create_access_token
from app.core.dependencies import CurrentUserEmail, DBSession

router = APIRouter()


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(payload: schemas.UserCreate, db: DBSession) -> schemas.UserResponse:
    existing = await service.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = await service.create_user(db, payload.email, payload.password)
    return user


@router.post("/login", response_model=schemas.Token)
async def login(payload: schemas.LoginRequest, db: DBSession) -> schemas.Token:
    user = await service.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(subject=user.email)
    return schemas.Token(access_token=token)


@router.get("/me", response_model=schemas.UserResponse)
async def get_me(
    current_user_email: CurrentUserEmail, db: DBSession
) -> schemas.UserResponse:
    user = await service.get_user_by_email(db, current_user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
