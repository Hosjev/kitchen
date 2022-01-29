from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    # Retrieve ingredients from local DB
    db = get_db()
    booze = db.execute(
        'SELECT b.id, b.name'
        ' FROM booze b '
    ).fetchall()
    boozeless = db.execute(
        'SELECT b.id, b.name'
        ' FROM boozeless b '
    ).fetchall()
    ingreds = db.execute(
        'SELECT i.id, i.name'
        ' FROM ingredients i '
    ).fetchall()

    # Form request
    if request.method == 'POST':
        alcohol = request.form['booze']
        #non_alcohol = request.form['boozeless']
        ingredients = list()
        for k,v in request.form.items():
            if k.startswith("ingred"):
                ingredients.append(v)
        error = None

        #if alcohol and non_alcohol:
            #flash('Please be boozy ... or not.')
        #to_taste = alcohol if alcohol else non_alcohol
        to_taste = alcohol
        all_ingredients = [to_taste] + ingredients

        if not all_ingredients:
            error = 'Error'

        if error is not None:
            flash(error)
        else:
            current_app.logger.info(all_ingredients)
            return redirect(url_for('home.drinks'))

    return render_template('home/index.html',
            booze=booze,
            boozeless=boozeless,
            ingreds=ingreds)

@bp.route('/drinks')
def drinks(ingredients):
    URL = "http://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Blended%20Whiskey"
    return render_template('home/drinks.html')
