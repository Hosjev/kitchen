import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_db():
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read())

    db.commit()
    cursor.close()
    db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Create CLI command to initialize the database."""
    init_db()
    click.echo('Initialized the database.')


def get_db():
    """Store database connection object in 'g' if not present."""
    db_args = {
            'host': current_app.config['HOST'],
            'port': current_app.config['PORT'],
            'database': current_app.config['DATABASE'],
            'user': current_app.config['USER'],
            'password': current_app.config['PSWD'],
            'sslmode': current_app.config['SSLMODE']
            }
    if 'db' not in g:
        g.db = psycopg2.connect(**db_args)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """Register teardown and init-db cli functionality."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
