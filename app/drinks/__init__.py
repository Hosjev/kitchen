import json

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)
from app.lib.db import get_db
from app.lib import common

bp = Blueprint('drinks', __name__, url_prefix='/api/v1/drinks')


@bp.route('/id/', methods=['GET', 'POST'])
def _drink_api_id():
    """Return single recipe by ID"""
    id = request.args.get('i')
    db = get_db()
    desc, _tmp = common._query_by_id(db, id)
    common.log_client(request)
    drink = dict(zip([x.name for x in desc], _tmp[0])) 
    drink['created'] = drink['created'].ctime()
    return json.dumps(drink, indent=4)


@bp.route('/recipes/', methods=['GET'])
def _drink_api_all():
    """Return all drinks by ID and name"""
    db = get_db()
    drinks = common._query_all_cocktails(db)
    common.log_client(request)
    return json.dumps(dict(drinks))


@bp.route('/recipes/ingredients/', methods=['POST'])
def _drink_api_ingreds(ingredients: list):
    """Return drinks based on ingredients"""
    # log_client
    # input = request.get_json()
    # first _query_by_ingredients(list)
    return
