"""auto

Revision ID: 0002
Revises: 0001
Create Date: 2022-05-19 00:48:32.201723

"""
from alembic import op
from mviews import (
    Balance,
    balance_query,
)

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    view_query_string = str(
        balance_query.compile(compile_kwargs={"literal_binds": True})
    )

    op.execute(
        f"CREATE MATERIALIZED VIEW {Balance.__table__.name} "
        f"AS {view_query_string}"
    )


def downgrade():
    op.execute(f"DROP MATERIALIZED VIEW {Balance.__table__.name}")
