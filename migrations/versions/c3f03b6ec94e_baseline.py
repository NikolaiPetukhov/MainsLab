"""baseline

Revision ID: c3f03b6ec94e
Revises: 
Create Date: 2022-11-17 23:34:40.137156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3f03b6ec94e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'orgs',
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String, index=True, nullable=False),
        sa.Column("client_name", sa.String, index=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('orgs')
