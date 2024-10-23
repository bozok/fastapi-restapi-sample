# Alembic settings:

### Initialize alembic:
`alembic init alembic`

### Configure alembic

- change db path with original in alembic.ini

    `sqlalchemy.url = sqlite:///./todos.db`

- Remove the following line from env.py file and correct the indentation of the line below it:

    `if config.config_file_name is not None:`
- Import metadata from database.py and assign it:

    `target_metadata = metadata`
- Create revision on command line after making changes to your tables:

    `alembic revision -m "create phone number column in users table"`


### Upgrade db changes

- Go to created revision file, and update the `def upgrade()` function:

    ```python
    def upgrade() -> None:
        op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    ```

- Run upgrade command with revision number:

    `alembic upgrade <revision_id>`

### Downgrade db changes

- Go to created revision file, and update the `def downgrade()` function:

    ```python
    def downgrade():
        op.drop_column('users', 'phone_number')
    ```

- Run downgrade command:

    `alembic downgrade -1`



### Note:
If you mess up anything in upgrading/downgrading things, there is a table `alembic_version` in your database that holds the revision history.
You can query this table to see where you messed up. If you're still struggling to find the issue then simply drop that table, remove the alembic related files from your project and initialize alembic again.