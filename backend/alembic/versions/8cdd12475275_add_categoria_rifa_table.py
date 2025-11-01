"""add categoria_rifa table

Revision ID: 8cdd12475275
Revises: 273499e3b2be
Create Date: 2025-11-01 13:04:17.209917+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cdd12475275'
down_revision: Union[str, Sequence[str], None] = '273499e3b2be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('categoria_rifa',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('color', sa.String(length=32), nullable=True),
    sa.Column('valor_boleta', sa.Integer(), nullable=False),
    sa.Column('total_recaudo', sa.Integer(), nullable=True),
    sa.Column('rake', sa.Numeric(precision=5, scale=4), nullable=True),
    sa.Column('fondo_premios', sa.Integer(), nullable=True),
    sa.Column('premio_por_ganador', sa.Integer(), nullable=True),
    sa.Column('comentario', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('categoria_rifa')
