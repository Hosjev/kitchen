from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db
from .cocktails import ExternalApi

bp = Blueprint('home', __name__)

# Global URLs
# by ingredient
URL_IG = "https://www.thecocktaildb.com/api/json/v2/9973533/filter.php?i="
# by ID
URL_ID = "https://www.thecocktaildb.com/api/json/v2/9973533/lookup.php?i="



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
            #flash('Please be boozy ... or eazy-classy.')
        #to_taste = alcohol if alcohol else non_alcohol
        to_taste = alcohol
        all_ingredients = [to_taste] + ingredients

        if not all_ingredients:
            error = 'Error'

        if error is not None:
            flash(error)
        else:
            current_app.logger.info(all_ingredients)
            return drinks(all_ingredients)

    return render_template('home/index.html',
            booze=booze,
            boozeless=boozeless,
            ingreds=ingreds)


@bp.route('/api/v1')
def api_drinks(ingredients):
    # Stub for API
    return


@bp.route('/drinks')
def drinks(ingredients):
    response = None
    url = URL_IG + ",".join(ingredients)
    wb = ExternalApi.WebResource()
    try:
        response = wb.get_url(url)
    except Exception as e:
        current_app.logger.error(e)
        flash(e)
        return redirect(url_for('index'))

    current_app.logger.info(f"Url: {url}:{response.status_code}")

    if response.json()['drinks'] == 'None Found':
        flash("No drinks found based on ingredients.")
        return redirect(url_for('index'))
    else:
        avail_drinks = list()
        array_ids = [ item['idDrink'] for item in response.json()['drinks']]
        array_ids = array_ids[:8]
        for d_id in array_ids:
            try:
                url = URL_ID + d_id
                response = wb.get_url(url)
            except Exception as e:
                current_app.logger.error(e)
            finally:
                avail_drinks += response.json()['drinks']
        current_app.logger.info(f"Number of Avail: {len(avail_drinks)}")

    return render_template('home/drinks.html', drinks=avail_drinks)



def get_drinks_by_ingredient(ingredients):
    data = dict()
    return
