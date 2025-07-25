"""empty message

Revision ID: cae0a8ddeef3
Revises: bf7fa81685a6
Create Date: 2025-07-24 00:54:56.986683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cae0a8ddeef3'
down_revision = 'bf7fa81685a6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=False))
        batch_op.create_unique_constraint("uq_user_email", ['email'])  # <-- Named constraint here

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint("uq_user_email", type_='unique')  # <-- Use same name here
        batch_op.drop_column('email')

    # ### end Alembic commands ###
