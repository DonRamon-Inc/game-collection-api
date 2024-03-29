"""aumentando a string da url_capa

Revision ID: e5a28dcac177
Revises: 9e7f7c3bdf66
Create Date: 2022-10-04 16:48:03.695987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a28dcac177'
down_revision = '9e7f7c3bdf66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jogo_favorito', 'url_capa')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jogo_favorito', sa.Column('url_capa', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
