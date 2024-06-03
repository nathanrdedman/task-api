from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from task_api.api.schema import Token, User
from task_api.auth.oauth import (
    authenticate_user,
    fake_users_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_active_user,
    create_access_token,
)
from datetime import datetime, timedelta, timezone
from task_api.auth.oauth import oauth2_scheme, get_current_user
# from task_api.db.models import User
from task_api.db.operation import read_task, delete_task

app = FastAPI()


@app.get("/healthz")
async def root():
    return {"status": "OK"}


@app.get("/task/{task_id}")
async def get_task(token: Annotated[str, Depends(oauth2_scheme)], task_id: int):
    return read_task(task_id=task_id)


@app.post("/task/{task_id}")
async def create_task(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.delete("/task/{task_id}")
async def del_task(token: Annotated[str, Depends(oauth2_scheme)], task_id: int):
    return delete_task(task_id=task_id)

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/tasks/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
