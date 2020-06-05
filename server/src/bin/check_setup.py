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
    import db
    from settings import Database
    from utils.log import log, log_colors

    setup_message = '''
        Your database is not set up. Please run:

        docker-compose run server python bin/db_reset.py
    '''

    migrate_message = '''
        Your database is out of date. Please run:

        docker-compose run server python bin/db_migrate.py
    '''

    version = db.version()
    latest_version = 0  # will come from the migrate module

    if version == -1:
        log(setup_message, color=log_colors.FAIL, dedent=True)
        sys.exit(1)

    elif version < latest_version:
        log(migrate_message, color=log_colors.FAIL, dedent=True)
        sys.exit(1)

    else:
        log('DB looks good')


def show_db_contents():
    import db
    from tabulate import tabulate
    from settings import Socrata

    years = sorted(Socrata.DATASET_IDS.keys())
    info_rows = db.info.rows()['byYear']
    rows = [info_rows.get(year, 0) for year in years]

    print(tabulate({
        'year': years,
        'requests': rows,
    }, tablefmt='psql', headers='keys'))


if __name__ == '__main__':
    from utils.log import log_heading
    import time

    time.sleep(1)

    log_heading('checks')
    check_env()
    check_db()

    log_heading('database contents')
    show_db_contents()

    import pb
    if not pb.enabled:
        pb.clear_data()
    elif not pb.available():
        log_heading('populating picklebase', spacing=(1, 0))
        pb.populate()

    import settings
    log_heading('settings')
    settings.show()
