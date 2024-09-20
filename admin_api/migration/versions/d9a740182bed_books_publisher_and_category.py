"""Books publisher and category

Revision ID: d9a740182bed
Revises: 6b6094cc5b40
Create Date: 2024-09-18 09:44:41.683733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9a740182bed'
down_revision: Union[str, None] = '6b6094cc5b40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('book_publisher_key', 'book', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('book_publisher_key', 'book', ['publisher'])
    # ### end Alembic commands ###
