import os
import sys
sys.path.append("/home/hosjev/.local/lib/python3.6/site-packages")

from flask import Flask, jsonify

from .cocktails import ExternalApi


URL = "http://www.thecocktaildb.com/api/json/v1/1/list.php?i=list"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # our main ingress
    @app.route("/drinks")
    def get_drinks():
        try:
            wb = ExternalApi.WebResource(URL)
            wb.get_url()
            data = wb.json_data()
        except:
            return "Nothing found."
        return jsonify(data)

    # Placeholder for future development (private DB)
    #from . import auth
    #app.register_blueprint(auth.db)

    # Initialize command for DB population
    from . import db
    db.init_app(app)

    # Initialize main page and register
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    # Add blueprint or route for API
    #   and add limiter
    # @app.route('/api/v1/drinks')

    return app
