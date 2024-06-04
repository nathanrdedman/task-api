from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic.types import List
from task_api.api.schema import Task, TaskBase, Token, User, UserCreate, TaskCreate
from task_api.auth.oauth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    oauth2_scheme,
)

from task_api.db.connect import engine, get_db
from task_api.db.operation import (
    archive_task,
    modify_task_status,
    read_status_values,
    read_task,
    read_tasks,
    write_task,
    new_user,
)

app = FastAPI()


@app.get("/healthz")
async def root():
    return {"status": "OK"}


@app.get("/task/{task_id}", response_model=Task)
async def get_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    db: Session = Depends(get_db),
):
    return read_task(db=db, task_id=task_id, user_id=current_user.id)


@app.get("/task_status")
async def get_task_status(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return read_status_values()


@app.patch("/task/{task_id}/status/{status}", response_model=Task)
async def task_status(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
):
    return modify_task_status(
        db=db, task_id=task_id, user_id=current_user.id, status=status
    )


@app.get("/task/", response_model=List[Task])
async def get_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return read_tasks(db=db, user_id=current_user.id)


@app.post("/task/", response_model=Task)
async def create_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    return write_task(db=db, description=task.description, user_id=current_user.id)


@app.delete("/task/{task_id}", response_model=Task)
async def delete_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    db: Session = Depends(get_db),
):
    return archive_task(db=db, task_id=task_id, user_id=current_user.id)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
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


@app.get("/user", response_model=User)
async def get_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return current_user


@app.post("/user", response_model=User)
async def create_user(
    create_user: UserCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return new_user(db=db, user=create_user)
