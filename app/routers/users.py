import json
from datetime import timedelta
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, status, requests
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import Token, User, UserCreate
from app.database import get_session
from app.oauth2 import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    CLEARBIT_API_KEY,
    CLEARBIT_URL,
    authenticate_user, 
    create_access_token, 
    get_current_user
)
from app.crud import get_user_by_username, create_user, get_user_by_email, add_additional_info


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/signup", response_model=User)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_session)): 
    db_user = await get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already exists"
        )
    db_user = await get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already exists"
        )
    new_user = await create_user(db=db, user=user)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLEARBIT_URL}{new_user.email}", headers={"Authorization": f"Bearer {CLEARBIT_API_KEY}"})
        if response.status_code == 200:
            try:
                data = {}
                data["fullName"] = json.loads(response.text)["person"]["name"]["fullName"]
                data["givenName"] = json.loads(response.text)["person"]["name"]["givenName"]
                data["familyName"] = json.loads(response.text)["person"]["name"]["familyName"]
                data["location"] = json.loads(response.text)["person"]["location"]
                data["avatar"] = json.loads(response.text)["person"]["avatar"]
                new_user = await add_additional_info(db=db, data=data, user=new_user)
            except KeyError:
                pass
            
    return new_user


@user_router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    user = await get_user_by_username(db=db, username=current_user.username)
    return user