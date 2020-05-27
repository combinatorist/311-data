from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import event
from settings import Database


engine = None if Database.URL is None else create_engine(Database.URL)


Session = sessionmaker(bind=engine)


def exec_sql(sql):
    with engine.connect() as conn:
        return conn.execute(text(sql))


if Database.LOG_QUERIES:
    event.listen(
        engine,
        'before_cursor_execute',
        lambda conn, cursor, statement, parameters, context, executemany:
            print(statement))


if Database.LOG_CONNECTIONS:
    import os

    def on_checkout(*args, **kwargs):
        print('process id {} checkout'.format(os.getpid()), flush=True)

    def on_checkin(*args, **kwargs):
        print('process id {} checkin'.format(os.getpid()), flush=True)

    event.listen(engine, 'checkout', on_checkout)
    event.listen(engine, 'checkin', on_checkin)
