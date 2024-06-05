"""Initial tables creation

Revision ID: 961b4952e8cf
Revises: 
Create Date: 2024-06-04 12:20:29.623320

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import Sequence as SQL_Sequence

from alembic import op
from task_api.auth.utils import hash_password

# revision identifiers, used by Alembic.
revision: str = "961b4952e8cf"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:

    user_table = op.create_table(
        "user",
        sa.Column(
            "id", sa.Integer, primary_key=True, nullable=False, autoincrement=True
        ),
        sa.Column("username", sa.String(1000), nullable=False, unique=True),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(1000), nullable=False, unique=True),
    )

    op.create_table(
        "task",
        sa.Column(
            "id", sa.Integer, primary_key=True, nullable=False, autoincrement=True
        ),
        sa.Column("description", sa.String(1000), nullable=False),
        sa.Column("user_id", sa.Integer()),
        sa.Column("status", sa.String(15), nullable=False),
    )

    op.create_table(
        "task_deleted",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("description", sa.String(1000), nullable=False),
        sa.Column("user_id", sa.Integer()),
        sa.Column("status", sa.String(15), nullable=False),
    )

    op.bulk_insert(
        user_table,
        [
            {
                "id": 1,
                "username": "admin",
                "full_name": "Admin account",
                "email": "admin@email.com",
                "hashed_password": hash_password("admin123"),
            },
            {
                "id": 2,
                "username": "user_1",
                "full_name": "User One",
                "email": "an@email.com",
                "hashed_password": hash_password("iamuser1"),
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("task")
    op.drop_table("task_deleted")
    op.drop_table("user")
    op.execute("drop sequence TASK_ID_SEQ")
