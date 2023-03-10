"""init

Revision ID: e0aaaf4ce6c5
Revises: 
Create Date: 2023-02-08 19:50:34.673305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e0aaaf4ce6c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('proposal_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('weight', sa.Float(), server_default=sa.text('1.0'), nullable=True),
    sa.PrimaryKeyConstraint('proposal_id', 'user_id')
    )
    op.create_table('proposals',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('number', sa.String(length=12), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('registered_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('problem_description', sa.Text(), nullable=False),
    sa.Column('proposal_content', sa.Text(), nullable=False),
    sa.Column('expected_result', sa.Text(), nullable=False),
    sa.Column('category', sa.Enum('WITH_ECO', 'WITHOUT_ECO', 'IMPORTANT', name='proposalcategory'), nullable=False),
    sa.Column('initiator_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_verified', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('email', sa.String(length=264), nullable=False),
    sa.Column('fullname', sa.String(length=264), nullable=False),
    sa.Column('department', sa.String(length=264), nullable=False),
    sa.Column('post', sa.String(length=264), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'DIRECTOR', 'MEMBER', 'CONTROLLER', 'EMPLOYEE', name='role'), server_default='EMPLOYEE', nullable=True),
    sa.Column('hashed_password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('verifications',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('controller_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('result', sa.Enum('REJECTED', 'ACCEPTED', name='verificationresult'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verifications')
    op.drop_table('users')
    op.drop_table('proposals')
    op.drop_table('authors')
    # ### end Alembic commands ###
