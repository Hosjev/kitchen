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
    """This main page view retrieves 3 dicts from the sqlite instance.
    The selection options require only an alcohol type to be chosen.
    Future releases will take a strict alcohol or non-alcohol type. 
    Ingredients are optional.
    """
    if request.method == 'GET': log_client(request)

    # Database fetch
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
        'SELECT doc.name as category, group_concat(do.id||","||do.name,";") collection'
        ' FROM drink_other do'
        ' INNER JOIN drink_other_cats doc ON doc.id = do.cat_id'
        ' GROUP BY category'
        ' ORDER BY doc.priority'
    ).fetchall()

    # Form request
    if request.method == 'POST':
        alcohol = request.form['booze']
        #non_alcohol = request.form['boozeless']
        ingredients = [v for k,v in request.form.items() if k.startswith('ingred')]
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


@bp.route('/v1/')
def api_drinks(ingredients):
    """
    Stub our API (pre json response -- sanitize results)
      (swagger-ish)
    TODO: start lovingly embracing YAML; turn this endpoint into its own blueprint
    {
        "info": {
            "version": "1.0",
            "title": "Drinks Recipe(s) Endpoint"
        },
        "basePath": "/v1",
        "schemes": ["http", "https"],
        "consumes": [ "application/json" ],
        "produces": [ "application/json" ],
        "paths": {
            "/v1/drinks": {
                "get": {
                    "summary": "Get recipes based on ingredients",
                    "parameters": [
                        {
                            "name": "offset",
                            "type": "integer"
                        },
                        {
                            "name": "limit",
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "JSON object"
                        },
                        "204": {
                            "description": "JSON object (none found based on parameters)"
                        }
                    }
                }
            }
        }
    }
    """
    return


@bp.route('/drinks/')
def drinks(ingredients):
    """Build id list from external api call. Build page from call details."""
    # TODO:
    #   1. defer this activity to an 'in progress' page
    #   2. store final ID results in local cache (hit/miss)
    #   3. future features will req Sql)
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
    """Function to register messages with flash and redirect to main."""
    current_app.logger.error(e)
    flash(e)
    return redirect(url_for('index'))


def log_client(r):
    if not r.environ.get('HTTP_X_FORWARDED_FOR'):
        req_ip = r.environ['REMOTE_ADDR']
    else:
        req_ip = r.environ['HTTP_X_FORWARDED_FOR']
    current_app.logger.info(f"connection request from client: {req_ip}")
