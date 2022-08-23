from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)


def _query_by_ingredients(db: object, all_ingredients: list) -> tuple:
    # Form query
    cur = _get_cursor(db)
    cur.execute(
            "SELECT drink_id, name, type, container, image, instructions, ingredients"
            " FROM be_drinks"
            " WHERE (ingredients)::jsonb ? ALL(ARRAY[%s])",
            (all_ingredients,)
    )
    drinks = cur.fetchall()
    _close_cursor(cur)
    return drinks


def _query_all_cocktails(db: object) -> tuple:
    """Return ID and names"""
    cur = _get_cursor(db)
    cur.execute(
            "SELECT id, name"
            " FROM be_drinks"
    )
    drinks = cur.fetchall()
    return drinks


def _query_by_id(db: object, id: int) -> tuple:
    """Return full recipe by ID"""
    cur = _get_cursor(db)
    cur.execute(
            "SELECT *"
            " FROM be_drinks"
            " WHERE id = %s",
            (id,)
    )
    drink = cur.fetchall()
    return cur.description, drink


def _get_cursor(db):
    return db.cursor()


def _close_cursor(cursor) -> None:
    cursor.close()


def log_client(r):
    if not r.environ.get('HTTP_X_FORWARDED_FOR'):
        req_ip = r.environ['REMOTE_ADDR']
    else:
        req_ip = r.environ['HTTP_X_FORWARDED_FOR']
    current_app.logger.info(f"connection request from client: {req_ip}")
