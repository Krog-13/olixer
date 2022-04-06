from os import environ, path
from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Database config
DATABASE_HOST = environ.get('DATABASE_HOST')
DATABASE_USERNAME = environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
DATABASE_PORT = environ.get('DATABASE_PORT')
DATABASE_NAME = environ.get('DATABASE_NAME')

SQL_QUERIES_FOLDER = 'sql'



API_KEY = '5209703716:AAF3DJmQqNRyq4-anRaVO6kCyNcft8kYHFM'
SOURCE_URL = 'https://www.olx.kz'

query_url = "ELECT url FROM urls WHERE type_url=%(type)s"
arg_url = {'type':'simple'}

selector = {
    'title': 'h1[data-cy="ad_titleee"]',
    'text': 'div[data-cy="ad_description"]>div',
    'datetime': 'span[data-cy="ad-posted-at"]',
    'price': 'div[data-testid="ad-price-container"]>h3',
}

# start pgadmin-web sudo /usr/pgadmin4/bin/setup-web.sh