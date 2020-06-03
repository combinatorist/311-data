import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))


def check_env():
    from os.path import isfile
    from utils.log import log, log_colors

    env_dir = join(dirname(__file__), '../..')
    env_file = join(env_dir, '.env')

    if isfile(env_file):
        log('.env file found')
    else:
        log('''\
            Your .env file is missing. Please run:

            cp .env.example .env
        ''', color=log_colors.FAIL, dedent=True)
        sys.exit(1)


def check_db():
    '''
    Check whether the DB is in the right format.
    '''
    import sys
    import db
    from utils.log import log, log_colors

    try:
        db.exec_sql('SELECT * FROM requests LIMIT 1')
        log('DB looks good')
    except Exception:
        log('''
            Your database is out of date. To fix, set
            INGEST_YEARS in your .env file to whatever years
            you want to ingest, and then run:

            docker-compose run server python bin/ingest.py
        ''', color=log_colors.FAIL, dedent=True)
        sys.exit(1)


if __name__ == '__main__':
    from utils.log import log_heading
    import time

    time.sleep(1)

    log_heading('checks')
    check_env()
    check_db()

    import pb
    if not pb.enabled:
        pb.clear_data()
    elif not pb.available():
        log_heading('populating picklebase', spacing=(1, 0))
        pb.populate()

    import settings
    log_heading('settings')
    settings.show()
