import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



def create_app(test_config=None):
    """Create and return a Flask app factory object.

    Flask treats (__name__) as the package as opposed
    to calling 'app.py' and defining app within. To
    use this method of an app factory with proxies,
    reference the application as such:
        gunicorn <options> "app:create_app()"

    To do so with Beanstalk, add the following with 
    quotes escaped in a Procfile at app base:
        gunicorn <options> \"app:create_app()\"

    Keyword argument(s):
    test_config -- the environment (default None)
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        API_KEY=os.environ.get('API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    # Load configs from classes within config.py if exists,
    # else load from argument
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Rate Limiting defaults
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["300/day", "100/hour", "30/minute"]
    )
    limiter.init_app(app)

    # Initialize command for DB population
    from . import db
    db.init_app(app)

    # Register main page and add endpoint to app object
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    # Add blueprint / route for API
    #   and add limiter
    # @app.route('/api/v1/drinks/')
    # @limiter.limit("60 per hour")

    return app
