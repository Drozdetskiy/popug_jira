"""auto

Revision ID: 0001
Revises:
Create Date: 2022-05-12 14:05:25.668742

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=50), nullable=False),
        sa.Column(
            "username",
            sa.String(length=50),
            server_default=sa.text("''"),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.Enum("EMPLOYEE", "ADMIN", "MANAGER", name="userroles"),
            nullable=True,
        ),
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column(
            "description",
            sa.Text(),
            server_default=sa.text("''"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("OPEN", "DONE", name="taskstatus"),
            server_default=sa.text("'OPEN'"),
            nullable=False,
        ),
        sa.Column("assignee_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["assignee_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tasks")
    op.drop_table("users")
    # ### end Alembic commands ###
