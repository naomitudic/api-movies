"""add directors table aand director_id to movies and fix

Revision ID: 8dff36792899
Revises: 8a1b8690f992
Create Date: 2026-09-26 20:13:30.290773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8dff36792899'
down_revision: Union[str, Sequence[str], None] = '8a1b8690f992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('directors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('biography', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_directors_id'), 'directors', ['id'], unique=False)
    op.create_index(op.f('ix_directors_name'), 'directors', ['name'], unique=False)

    with op.batch_alter_table('movie') as batch_op:
        batch_op.add_column(sa.Column('director_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_movie_director_id_directors',
            'directors',
            ['director_id'],
            ['id'],
            ondelete='SET NULL',
        )
        batch_op.drop_index(op.f('ix_movie_director'))
        batch_op.drop_column('director')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('movie') as batch_op:
        batch_op.add_column(sa.Column('director', sa.VARCHAR(length=100), nullable=True))
        batch_op.drop_constraint('fk_movie_director_id_directors', type_='foreignkey')
        batch_op.drop_column('director_id')
        batch_op.create_index(op.f('ix_movie_director'), ['director'], unique=False)
    op.drop_index(op.f('ix_directors_name'), table_name='directors')
    op.drop_index(op.f('ix_directors_id'), table_name='directors')
    op.drop_table('directors')
    # ### end Alembic commands ###
