import asyncio

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)
from app.db import get_db
from .cocktails import webresource

bp = Blueprint('home', __name__)


# Global
# URL by ingredient
URL_IG = "https://www.thecocktaildb.com/api/json/v2/KEY/filter.php?i="
# URL by ID
URL_ID = "https://www.thecocktaildb.com/api/json/v2/KEY/lookup.php?i="



@bp.route('/', methods=('GET', 'POST'))
def index():
    """This main page view retrieves 3 dicts from the instance sqlite
    database then draws them onto the page. The selection
    options require only an alcohol type to be chosen. Future
    releases will take a strict alcohol or non-alcohol type. 
    Ingredients are optional.
    """
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

        # TODO: if alcohol and non_alcohol:
            # flash('Please be boozy ... or eazy-classy.')
            # return redirect(url_for('index'))
        # to_taste = alcohol if alcohol else non_alcohol
        to_taste = alcohol
        all_ingredients = [to_taste] + ingredients

        if not all_ingredients:
            error = f'Error: {all_ingredients}'

        if error is not None:
            flash(error)
        else:
            return drinks(all_ingredients)

    return render_template('home/index.html',
            booze=booze,
            boozeless=boozeless,
            ingreds=ingreds)


@bp.route('/api/v1')
def api_drinks(ingredients):
    # Stub for API (sanitize results)
    return


@bp.route('/drinks')
def drinks(ingredients):
    """Build id list from GET. Build page from GET details."""
    # TODO: defer this activity to a 'in progress' page
    response = None
    url = URL_IG.replace('KEY', current_app.config['API_KEY']) + ",".join(ingredients)
    wb = webresource.HTTPSync()
    try:
        response = wb.get_url(url)
    except Exception as e:
        return register_response(e)

    current_app.logger.info(f"Url: {url}:{response.status_code}")

    if response.json()['drinks'] == 'None Found':
        return register_response(f"No drinks found based on ingredients: {', '.join(ingredients)}")
    else:
        avail_drinks = list()
        array_ids = [ item['idDrink'] for item in response.json()['drinks']][:20]
        # Asynchronous http call(s) using aiohttp
        url_id = URL_ID.replace('KEY', current_app.config['API_KEY'])
        urls = [url_id + i for i in array_ids]
        try:
            results = []
            wb = webresource.HTTPAsync()
            asyncio.run(wb.bulk_get(urls, results))
        except Exception as e:
            return register_response(e)
        finally:
            # Parse drinks
            for d in results:
                if isinstance(d, dict) and d['drinks']:
                    avail_drinks += d['drinks']
                else: current_app.logger.error(f"Error for request from external API: {d}")
        current_app.logger.info(f"Number of Avail: {len(avail_drinks)}")

    return render_template('home/drinks.html', drinks=avail_drinks)


def register_response(e):
    current_app.logger.error(e)
    flash(e)
    return redirect(url_for('index'))
