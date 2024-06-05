"""Main FastAPI file"""

from datetime import timedelta
from typing import Annotated, Optional

from fastapi import (  # pylint: disable=import-error
    Depends,
    FastAPI,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm  # pylint: disable=import-error
from pydantic.types import List  # pylint: disable=import-error
from sqlalchemy.orm import Session  # pylint: disable=import-error

from task_api.api.schema import Task, TaskCreate, Token, User, UserCreate
from task_api.auth.oauth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from task_api.db.connect import get_db
from task_api.db.operation import (
    archive_task,
    modify_task_status,
    new_user,
    read_status_values,
    read_task,
    read_tasks,
    write_task,
)

app = FastAPI()


@app.get("/")
async def root():
    """Base route response

    Returns:
        dict: URL routes
    """
    return {
        "info": "API to CRUD operations for task management",
        "urls": {"/docs": "REST Documentation (Swagger)", "/healthz": "Status check"},
    }


@app.get("/healthz")
async def healthz():
    """Status check for API
    Used when part of deployment (k8s) for
    pod health

    Returns:
        dict: status message
    """
    return {"status": "OK"}


@app.post("/task/", response_model=Task)
async def create_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task: TaskCreate,
    db: Session = Depends(get_db),
) -> Task:
    """Create a new task with the supplied task description.
    Newly created tasks are set with status='Pending'

    Args:
        Request body (TaskCreate): Payload with 'description' field.

    Raises:
        HTTPException: Failed to create new task

    Returns:
        Task: Newly created task object
    """
    try:
        task = write_task(db=db, description=task.description, user_id=current_user.id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create task for user '{current_user.username}': {err}",
        ) from err
    return task


@app.get("/task/{task_id}", response_model=Task)
async def get_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    db: Session = Depends(get_db),
) -> Task:
    """Given as task ID and authenicated user return the task found
    by task_id.

    Args:
        task_id (int): Task ID

    Raises:
        HTTPException: Task not found or not authorised

    Returns:
        Task: task object
    """
    try:
        task = read_task(db=db, task_id=task_id, user_id=current_user.id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task ({task_id=}) not found for user '{current_user.username}': {err}",
        ) from err
    return task


@app.delete("/task/{task_id}", response_model=Task)
async def delete_task(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    db: Session = Depends(get_db),
) -> Task:
    """Delete a task by moving to the deleted tasks table

    Args:
        task_id (int): Task ID

    Raises:
        HTTPException: Task does not exist or is not found for user

    Returns:
        Task: task object
    """
    try:
        archived_task = archive_task(db=db, task_id=task_id, user_id=current_user.id)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete task ({task_id=}) for user '{current_user.username}': {err}",
        ) from err
    return archived_task


@app.get("/task_status")
async def get_task_status(
    _: Annotated[User, Depends(get_current_active_user)],
) -> dict:
    """Given an authenticated user return the possible
    status options as a dictionary:
    {"code":"value"}

    Args:
        None

    Returns:
        dict: Status options
    """
    return read_status_values()


@app.patch("/task/{task_id}/status/{status}", response_model=Task)
async def task_status(
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    update_status: str,
    db: Session = Depends(get_db),
) -> Task:
    """Update the status of a task

    Args:
        task_id (int): Task ID
        update_status (str): Status to update to

    Raises:
        HTTPException: Failed to update task status

    Returns:
        Task: Updated task object
    """
    try:
        updated_task = modify_task_status(
            db=db, task_id=task_id, user_id=current_user.id, new_status=update_status
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update task status ({task_id=}\
            for user '{current_user.username}': {err}",
        ) from err
    return updated_task


@app.get("/task/", response_model=List[Task])
async def get_tasks(
    skip: Optional[int],
    limit: Optional[int],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
) -> List[Task]:
    """For an authenticated user to retrieve the
    full list of tasks with pagination.

    Args:
        skip (int): Offset for pagination
        limit (int): Max page size for pagination

    Returns:
        List[Task]: List of tasks
    """
    return read_tasks(db=db, user_id=current_user.id, skip=skip, limit=limit)  # type: ignore


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    """Given a set of user credentials

    Args:
        form_data: Form data contained username / password

    Raises:
        HTTPException: Username or password incorrect or not found

    Returns:
        Token: JWT token
    """
    user_in = authenticate_user(db, form_data.username, form_data.password)

    if not user_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_in.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/user", response_model=User)
async def get_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """Return the currently authenticated user details

    Args:
        None

    Returns:
        User: Currently authenticated user details
    """
    return current_user


@app.post("/user", response_model=User)
async def create_user(
    user_to_create: UserCreate,
    _: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
) -> User:
    """Create a new user with the supplied username, password and email.

    Payload should be of the format:
        {
            "username":"auser",
            "email":"auser@domain.com",
            "password:"secretpassword"
        }

    Args:
        Request body (UserCreate): Payload containing user details

    Raises:
        HTTPException: Username or email already exists

    Returns:
        User: Newly created user details (with ID)
    """
    try:
        created_user = new_user(db=db, user=user_to_create)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create new user '{user_to_create.username}':\
                Username or email already exists!",
        ) from err
    return created_user
