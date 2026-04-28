from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.Application.UseCase.LoginUseCase import LoginUseCase
from src.Application.UseCase.RegisterUseCase import RegisterUseCase
from src.Infrastructure.Delivery.Http.Schemas.TokenSchema import (
    TokenResponse,
    RegisterRequest,
    RegisterResponse,
)
from src.Infrastructure.DependencyInjection.MongoProviders import (
    get_login_use_case,
    get_register_use_case,
)

router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    use_case: RegisterUseCase = Depends(get_register_use_case),
):
    try:
        user = await use_case.execute(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
        )
        return RegisterResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUseCase = Depends(get_login_use_case)
):
    try:
        token_dto = await use_case.execute(
            email=form_data.username,
            password=form_data.password
        )
        return token_dto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )