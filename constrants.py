import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', '172.17.0.1')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')

PGSQL_HOST = os.getenv('PGSQL_HOST', '172.17.0.1')
PGSQL_PORT = os.getenv('PGSQL_PORT', '5432')
PGSQL_USER = os.getenv('PGSQL_USER', 'postgres')
PGSQL_PASSWORD = os.getenv('PGSQL_PASSWORD', '')


# INSERT FROM AT LEAST THIS ID
MIN_BEHAVIOUR_ID = os.getenv('MIN_BEHAVIOUR_ID', '1')
