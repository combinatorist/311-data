import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))


def check_env():
    '''
    Check whether .env exists. If not, copy it from .env.example
    '''
    from os.path import isfile
    import shutil
    from utils.log import log

    env_dir = join(dirname(__file__), '../..')
    env_file = join(env_dir, '.env')
    example_file = join(env_dir, '.env.example')

    if not isfile(env_file):
        log('.env missing, copying .env.example')
        shutil.copyfile(example_file, env_file)
    else:
        log('.env file found')


def check_db():
    '''
    Check whether the DB is in the latest format. If not, update it.
    '''
    import sys
    import db
    from utils.log import log, log_colors

    try:
        db.exec_sql('SELECT * FROM requests LIMIT 1')
        log('DB looks good')
    except Exception:
        message = '''
Your local database is out of date. To fix, set INGEST_YEARS in your
`.env` file to whatever years you want to ingest, and then run:

docker-compose run server python bin/ingest.py
'''
        log(message, color=log_colors.FAIL)
        sys.exit(1)


if __name__ == '__main__':
    from utils.log import log_heading
    import time

    time.sleep(1)

    log_heading('checks')
    check_env()
    check_db()

    import pb
    if pb.enabled and not pb.available():
        log_heading('populating picklebase', spacing=(1, 0))
        pb.populate()

    import settings
    log_heading('settings')
    settings.show()
