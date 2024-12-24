"""Initial migration

Revision ID: 4745e783d57d
Revises: 2d650bdc8319
Create Date: 2024-12-19 12:16:11.733880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4745e783d57d'
down_revision: Union[str, None] = '2d650bdc8319'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('AccountID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Email', sa.String(length=255), nullable=False),
    sa.Column('Password', sa.String(length=255), nullable=False),
    sa.Column('Name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('AccountID'),
    sa.UniqueConstraint('Email'),
    schema='analysisstate'
    )
    op.create_table('notes',
    sa.Column('NoteID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AccountID', sa.Integer(), nullable=True),
    sa.Column('CreationDate', sa.DateTime(), nullable=True),
    sa.Column('Text', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['AccountID'], ['analysisstate.account.AccountID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('NoteID'),
    schema='analysisstate'
    )
    op.create_table('results',
    sa.Column('ResultID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AccountID', sa.Integer(), nullable=True),
    sa.Column('AnalysisDate', sa.DateTime(), nullable=True),
    sa.Column('StressLevel', sa.Integer(), nullable=False),
    sa.Column('EmotionalState', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['AccountID'], ['analysisstate.account.AccountID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ResultID'),
    schema='analysisstate'
    )
    op.drop_table('results')
    op.drop_table('account')
    op.drop_table('notes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('NoteID', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('AccountID', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('CreationDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('Text', sa.TEXT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['AccountID'], ['account.AccountID'], name='notes_AccountID_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('NoteID', name='notes_pkey')
    )
    op.create_table('account',
    sa.Column('AccountID', sa.INTEGER(), server_default=sa.text('nextval(\'"account_AccountID_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('Email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('Password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('Name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('AccountID', name='account_pkey'),
    sa.UniqueConstraint('Email', name='account_Email_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('results',
    sa.Column('ResultID', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('AccountID', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('AnalysisDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('StressLevel', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('EmotionalState', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['AccountID'], ['account.AccountID'], name='results_AccountID_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ResultID', name='results_pkey')
    )
    op.drop_table('results', schema='analysisstate')
    op.drop_table('notes', schema='analysisstate')
    op.drop_table('account', schema='analysisstate')
    # ### end Alembic commands ###
