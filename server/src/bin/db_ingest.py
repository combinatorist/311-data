import sys
from os.path import join, dirname
sys.path.append(join(dirname(__file__), '..'))


def get_cli_args():
    from argparse import ArgumentParser

    parser = ArgumentParser(description='''
        Seed the database with data from the Socrata api.
        Run with no args to get all Socrata data.
    ''')

    parser.add_argument('--years',
        type=str,
        help='comma-separated years to download (defaults to all years)')

    parser.add_argument('--rows',
        type=int,
        help='number of rows to downlad per year (defaults to all rows)')

    parser.add_argument('--batch',
        type=int,
        help='number of rows per call to Socrata api (defaults to 50000)')

    return parser.parse_args()


def parse_years(years):
    from settings import Socrata
    all_years = sorted(list(Socrata.DATASET_IDS.keys()))

    if years is None:
        parsed = all_years
    else:
        try:
            parsed = [int(year) for year in years.split(',')]
        except Exception:
            sys.exit('Could not parse years to list of ints')
        else:
            parsed = [year for year in parsed if year in all_years]
            parsed = sorted(list(set(parsed)))

    return parsed


if __name__ == '__main__':
    import db

    args = get_cli_args()

    years = parse_years(args.years)
    rows = -1 if args.rows is None else args.rows
    batch = 50000 if args.batch is None else args.batch

    db.reset()
    db.requests.add_years(years, rows_per_year=rows, batch_size=batch)
