# Description
Flask API using Blueprints to build factory objects for kitchen HLOs.
Thus far:
* drinks
* food (in dev)

### Flask Details
(From __init__) Create and return a Flask app factory object.

Flask treats (__name__) as the package as opposed
to calling 'app.py' and defining app within. To
use this method of an app factory with proxies,
reference the application as such:
    gunicorn <options> "app:create_app()"

To do so with Beanstalk, add the following with
quotes escaped in a Procfile at app base:
    gunicorn <options> \"app:create_app()\"

### Integrations
* Postgres database holding schema, ex - recipe details
* Redis database holding images - keys built from type#image#file_name
* cocktail DB API key held only in DO

# Install
The entirety of this backend is run from Git into a DO droplet.

## Starting the App
All env variables and entrypoints are defined in DO dashboard.

## Local Development
1. clone repo
2. create virtual venv and source activate
3. pip install -r requirements.txt
4. run a docker-compose up -d for Redis and PG and implement schema
  a. docker exec -i flaskPGKitch psql -U <> -W <> -d <> < app/schema.sql
5. populate Redis with images python3 app/lib/redis/importImages.py <directory>
5. set all env variables for both connections dictated in Flask entrypoint
  a. export DATABASE_URL=localhost \
     DB_PORT=5432 \
     DATABASE=dbkitch \
     PG_USER=flaskuser \
     PG_PSWD=flaskpswd \
     REDIS_URL=redis://localhost:6379
6. update code
7. gunicorn "app:create_app()"

# TODO
* mocktails - rebrand
* remove restrictions on booze v not v ingreds
* paginate results
* AI integration ideas:
  * pairings with chosen ingred(s)
  * potential matches with ingred(s) post-results
  * textual
  * use voice-generated integration
