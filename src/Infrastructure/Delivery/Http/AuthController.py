from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.Application.UseCase.LoginUseCase import LoginUseCase
from src.Infrastructure.Delivery.Http.Schemas.TokenSchema import TokenResponse
from src.Infrastructure.DependencyInjection.MongoProviders import get_login_use_case

router = APIRouter()

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