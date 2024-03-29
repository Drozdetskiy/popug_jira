"""auto

Revision ID: 0001
Revises:
Create Date: 2022-05-18 02:26:26.666391

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
        "billing_cycles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=50), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE", "PROCESSED", "CLOSED", name="billingcyclestatus"
            ),
            server_default=sa.text("'ACTIVE'"),
            nullable=False,
        ),
        sa.Column(
            "started_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=50), nullable=False),
        sa.Column(
            "title",
            sa.String(length=50),
            server_default=sa.text("''"),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            server_default=sa.text("''"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
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
            "email",
            sa.String(length=100),
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
        "taskcosts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=50), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("credit_cost", sa.Integer(), nullable=False),
        sa.Column("debit_cost", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
        sa.UniqueConstraint("task_id"),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=50), nullable=False),
        sa.Column(
            "debit", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column(
            "credit", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer()),
        sa.Column("billing_cycle_id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("INCOME", "EXPENSE", "PAYMENT", name="transactiontypes"),
            server_default=sa.text("'INCOME'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["billing_cycle_id"],
            ["billing_cycles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("taskcosts")
    op.drop_table("users")
    op.drop_table("tasks")
    op.drop_table("billing_cycles")
    # ### end Alembic commands ###
