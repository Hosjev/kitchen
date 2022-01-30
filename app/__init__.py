import os
import sys
sys.path.append("/home/hosjev/.local/lib/python3.6/site-packages")

from flask import Flask



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        API_KEY=os.environ.get('API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
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
