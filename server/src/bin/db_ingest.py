import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))


if __name__ == '__main__':
    import db
    from settings import Ingest

    db.reset()
    db.requests.add_years(Ingest.YEARS)
