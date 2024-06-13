"""My first migration

Revision ID: ced9cc0776d9
Revises: 
Create Date: 2024-06-12 07:22:36.791849

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql # type: ignore

# revision identifiers, used by Alembic.
revision = 'ced9cc0776d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(length=280), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_likes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_table('comment_likes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('comment_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'comment_id')
    )
    op.drop_table('image')
    op.drop_table('likes')

    # Add created_at column with default value for existing rows
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=280),
               existing_nullable=False)
        batch_op.drop_constraint('fk_posts_comments', type_='foreignkey')
        batch_op.drop_constraint('fk_user_comment', type_='foreignkey')
        batch_op.create_foreign_key(None, 'posts', ['post_id'], ['id'])
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=128), nullable=True, server_default='Untitled Post'))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=280),
               existing_nullable=False)
        batch_op.drop_constraint('fk_users_posts', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    # Remove the server default after the columns have been populated
    op.alter_column('comments', 'created_at', server_default=None)
    op.alter_column('posts', 'created_at', server_default=None)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.TEXT(),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=128),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.TEXT(),
               type_=sa.String(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=128),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=128),
               type_=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.String(length=128),
               type_=sa.TEXT(),
               existing_nullable=False)

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_users_posts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('description',
               existing_type=sa.String(length=280),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.drop_column('created_at')
        batch_op.drop_column('title')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('fk_user_comment', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_posts_comments', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('description',
               existing_type=sa.String(length=280),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.drop_column('created_at')

    op.create_table('likes',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('likeable_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('likeable_type', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('liked_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='likes_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'likeable_id', 'likeable_type', name='likes_pkey')
    )
    op.create_table('image',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('image_url', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='fk_posts_image'),
    sa.PrimaryKeyConstraint('id', name='image_pkey')
    )
    op.drop_table('comment_likes')
    op.drop_table('post_likes')
    op.drop_table('images')
    # ### end Alembic commands ###
