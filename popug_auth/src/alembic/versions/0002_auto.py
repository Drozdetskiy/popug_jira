"""auto

Revision ID: 0002
Revises: 0001
Create Date: 2022-05-09 00:37:38.006506

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "event_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pid", sa.String(length=50), nullable=False),
        sa.Column(
            "entity",
            sa.Enum("USER", name="entities"),
            server_default=sa.text("'USER'"),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.Enum("ADDED", "ROLE_CHANGED", "DELETED", name="eventtitles"),
            nullable=False,
        ),
        sa.Column(
            "type",
            sa.Enum("BUSINESS_CALL", "DATA_STREAMING", name="eventtypes"),
            server_default=sa.text("'DATA_STREAMING'"),
            nullable=False,
        ),
        sa.Column(
            "version",
            sa.Integer(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column(
            "data", sa.JSON(), server_default=sa.text("'{}'"), nullable=False
        ),
        sa.Column(
            "processed",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("event_log")
    # ### end Alembic commands ###
