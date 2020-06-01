import pandas as pd
import db
import pb


DEFAULT_TABLE = 'requests'


def item_query(srnumber, table=DEFAULT_TABLE):

    if not srnumber or not isinstance(srnumber, str):
        raise Exception('srnumber must be provided')

    rows = db.exec_sql(f"""
        SELECT * FROM {table}
        WHERE srnumber = '{srnumber}'
    """)

    rows = [dict(row) for row in rows]

    if len(rows) > 0:
        return rows[0]
    else:
        return None


def standard_query(fields, filters, table=DEFAULT_TABLE):

    # parse filters
    startDate = filters.get('startDate')
    endDate = filters.get('endDate')
    requestTypes = filters.get('requestTypes')
    ncList = filters.get('ncList')

    # validate input
    if not isinstance(fields, list) or len(fields) == 0:
        raise Exception('fields must be provided')

    if (
        startDate is None or
        endDate is None or
        not isinstance(requestTypes, list) or
        not isinstance(ncList, list)
    ):
        raise Exception('invalid filters')

    # try picklebase
    if pb.available():
        return pb.query(table, fields, filters)

    # hit database
    fields = (', ').join(fields)
    requestTypes = (', ').join([f"'{rt}'" for rt in requestTypes])
    ncList = (', ').join([str(nc) for nc in ncList])

    return pd.read_sql(f"""
        SELECT {fields}
        FROM {table}
        WHERE
            createddate >= '{startDate}' AND
            createddate <= '{endDate}' AND
            requesttype IN ({requestTypes}) AND
            nc IN ({ncList})
    """, db.engine)


def comparison_query(fields, filters, table=DEFAULT_TABLE):

    # parse filters
    startDate = filters.get('startDate')
    endDate = filters.get('endDate')
    requestTypes = filters.get('requestTypes')
    ncList = filters.get('ncList', [])
    cdList = filters.get('cdList', [])

    # validate input
    if not isinstance(fields, list) or len(fields) == 0:
        raise Exception('fields must be provided')

    if (
        startDate is None or
        endDate is None or
        not isinstance(requestTypes, list) or
        not isinstance(ncList, list) or
        not isinstance(cdList, list)
    ):
        raise Exception('invalid filters')

    # try picklebase
    if pb.available():
        return pb.query(table, fields, filters)

    # hit database
    fields = (', ').join(fields)
    requestTypes = (', ').join([f"'{rt}'" for rt in requestTypes])

    if len(ncList) > 0:
        ncList = (', ').join([str(nc) for nc in ncList])
        where = f'nc IN ({ncList})'
    else:
        cdList = (', ').join([str(cd) for cd in cdList])
        where = f'cd IN ({cdList})'

    return pd.read_sql(f"""
        SELECT {fields}
        FROM {table}
        WHERE
            createddate >= '{startDate}' AND
            createddate <= '{endDate}' AND
            requesttype IN ({requestTypes}) AND
            {where}
    """, db.engine)
