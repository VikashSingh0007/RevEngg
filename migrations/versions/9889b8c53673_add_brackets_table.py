from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "9889b8c53673"
down_revision = "5c4996aeb2cb"
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Check if the 'brackets' table exists
    if not inspector.has_table("brackets"):
        op.create_table(
            "brackets",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("type", sa.String(length=80), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
    
    # Check if the 'bracket_id' column exists in the 'teams' table
    if 'bracket_id' not in [col['name'] for col in inspector.get_columns('teams')]:
        op.add_column("teams", sa.Column("bracket_id", sa.Integer(), nullable=True))
        op.create_foreign_key(
            None, "teams", "brackets", ["bracket_id"], ["id"], ondelete="SET NULL"
        )
    
    # Check if the 'bracket' column exists in the 'teams' table before dropping it
    if 'bracket' in [col['name'] for col in inspector.get_columns('teams')]:
        op.drop_column("teams", "bracket")
    
    # Check if the 'bracket_id' column exists in the 'users' table
    if 'bracket_id' not in [col['name'] for col in inspector.get_columns('users')]:
        op.add_column("users", sa.Column("bracket_id", sa.Integer(), nullable=True))
        op.create_foreign_key(
            None, "users", "brackets", ["bracket_id"], ["id"], ondelete="SET NULL"
        )
    
    # Check if the 'bracket' column exists in the 'users' table before dropping it
    if 'bracket' in [col['name'] for col in inspector.get_columns('users')]:
        op.drop_column("users", "bracket")
