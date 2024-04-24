from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add a new column without the unique constraint
    op.add_column("city", sa.Column("new_name", sa.String))

    # Copy data from the existing column to the new column
    connection = op.get_bind()
    connection.execute("UPDATE city SET new_name = name")

    # Remove the existing column
    op.drop_column("city", "name")

    # Rename the new column and add the unique constraint
    op.alter_column("city", "new_name", new_column_name="name")
    op.create_unique_constraint(None, "city", ["name"])


def downgrade():
    # Відкотити зміни, якщо це необхідно
    pass
