from dotenv import load_dotenv
from functools import partial
from utils.settings import env, to, show as show_module
show = partial(show_module, __import__(__name__))
load_dotenv()


class Version:
    MAJOR = 0
    MINOR = 1
    PATCH = 0


class Server:
    HOST = '0.0.0.0'
    PORT = env('PORT', to.INT)
    DEBUG = env('DEBUG', to.BOOL)
    WORKERS = env('WORKERS', to.INT)
    TMP_DIR = env('TMP_DIR', to.ABS_PATH)


class Database:
    VERSION = 0
    URL = env('DATABASE_URL')
    LOG_QUERIES = env('DATABASE_LOG_QUERIES', to.BOOL)
    LOG_CONNECTIONS = False


class Redis:
    ENABLED = env('REDIS_ENABLED', to.BOOL)
    URL = env('REDIS_URL')
    TTL_SECONDS = env('REDIS_TTL_SECONDS', to.INT)


class Picklebase:
    ENABLED = env('PICKLEBASE_ENABLED', to.BOOL)
    BATCH_SIZE = env('PICKLEBASE_BATCH_SIZE', to.INT)


class Picklecache:
    ENABLED = env('PICKLECACHE_ENABLED', to.BOOL)


class Github:
    TOKEN = env('GITHUB_TOKEN')
    ISSUES_URL = 'https://api.github.com/repos/hackforla/311-data/issues'
    PROJECT_URL = env('GITHUB_PROJECT_URL')
    SHA = env('GITHUB_SHA')


class Socrata:
    TOKEN = env('SOCRATA_TOKEN')
    TIMEOUT = 90
    ATTEMPTS = 5
    DOMAIN = 'data.lacity.org'
    DATASET_IDS = {
        2020: 'rq3b-xjk8',
        2019: 'pvft-t768',
        2018: 'h65r-yf5i',
        2017: 'd4vt-q4t5',
        2016: 'ndkd-k878',
        2015: 'ms7h-a45h'}


class Ingest:
    YEARS = env('INGEST_YEARS', to.LIST_OF_INTS)
    BATCH_SIZE = env('INGEST_BATCH_SIZE', to.INT)
    ROWS_PER_YEAR = env('INGEST_ROWS_PER_YEAR', to.INT)


class Slack:
    WEBHOOK_URL = env('SLACK_WEBHOOK_URL')
    ERROR_CODES = env('SLACK_ERROR_CODES', to.LIST_OF_INTS)
