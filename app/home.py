import asyncio
import base64

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)
import redis
from app.lib.db import get_db
from app.lib.redis.client import RedisFlask
from app.lib.images import ImageParser
from app.lib import webresource
from app.lib import common

bp = Blueprint('home', __name__)


# GLOBAL
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
    if request.method == 'GET': common.log_client(request)

    # Redis client
    redis = RedisFlask.connect(0)

    # Database fetch
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT b.id, b.name"
        " FROM booze b "
    )
    booze = cur.fetchall()
    cur.execute(
        "SELECT b.id, b.name"
        " FROM boozeless b "
    )
    boozeless = cur.fetchall()
    cur.execute(
        "SELECT drink_other_cats.name as category,"
        " ARRAY_AGG(drink_other.id||','||drink_other.name) collection"
        " FROM drink_other"
        " INNER JOIN drink_other_cats ON drink_other_cats.id = drink_other.cat_id"
        " GROUP BY category, priority"
        " ORDER BY priority "
    )
    _ingreds = cur.fetchall()
    cur.close()

    ingreds = {}
    for i in _ingreds: ingreds[i[0]] = sorted(i[1], key=lambda x: x.split(',')[1])

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
            # return drinks(all_ingredients)
            return get_local_drinks(redis, db, all_ingredients)

    return render_template('home/index.html',
            booze=booze,
            boozeless=boozeless,
            ingreds=ingreds)


def get_local_drinks(redis: redis.Redis, db: object, all_ingredients: list):
    # PG Query
    drinks = common._query_by_ingredients(db, all_ingredients)

    # Process response
    if not bool(drinks):
        return register_response(f"No drinks found based on ingredients: {', '.join(all_ingredients)}")
    else:
        drinks = parse_images(redis, drinks)
        current_app.logger.info(f"Number of Avail: {len(drinks)}")

    return render_template('home/drinks.html', drinks=drinks)


def get_api_drinks(ingredients):
    """Build id list from external api call. Build page from call details."""
    # Function retired in favor of Postgres calls
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


def parse_images(redis: redis.Redis, drinks: list) -> list:
    """Process images based on name from Redis.

    Args:
        drinks (list): an array of tuples
                       [(id, name, type, cont, image,...)]
    """
    newDrinks = asyncio.run(ImageParser().getAllImages(redis, drinks))
    #current_app.logger.warn(newDrinks)
    return newDrinks


def register_response(e):
    """Function to register messages with flash and redirect to main."""
    current_app.logger.error(e)
    flash(e)
    return redirect(url_for('index'))
