import pandas as pd
import db
import pb


DEFAULT_TABLE = 'requests'


def itemQuery(requestNumber, table=DEFAULT_TABLE):
    '''
    Returns a single request by its requestNumber.
    '''

    if not requestNumber or not isinstance(requestNumber, str):
        return {'Error': 'Missing request number'}

    rows = db.exec_sql(f"""
        SELECT * FROM {table}
        WHERE srnumber = '{requestNumber}'
    """)

    rows = [dict(row) for row in rows]

    if len(rows) > 0:
        return rows[0]
    else:
        return {'Error': 'Request number not found'}


# def standardFilters(startDate=None,
#                     endDate=None,
#                     requestTypes=[],
#                     ncList=[]):
#     '''
#     Generates filters for dates, request types, and ncs.
#     '''
#     if pb.available():
#         return {
#             'startDate': startDate,
#             'endDate': endDate,
#             'requestTypes': requestTypes,
#             'ncList': ncList}
#
#     requestTypes = (', ').join([f"'{rt}'" for rt in requestTypes])
#     ncList = (', ').join([str(nc) for nc in ncList])
#     return f"""
#         createddate >= '{startDate}' AND
#         createddate <= '{endDate}' AND
#         requesttype IN ({requestTypes}) AND
#         nc IN ({ncList})
#     """


def comparisonFilters(startDate=None,
                      endDate=None,
                      requestTypes=[],
                      ncList=[],
                      cdList=[]):
    '''
    Generates filters for the comparison endpoints.
    '''
    if pb.available():
        return {
            'startDate': startDate,
            'endDate': endDate,
            'requestTypes': requestTypes,
            'ncList': ncList,
            'cdList': cdList}

    requestTypes = (', ').join([f"'{rt}'" for rt in requestTypes])
    if len(ncList) > 0:
        ncList = (', ').join([str(nc) for nc in ncList])
        return f"""
            createddate >= '{startDate}' AND
            createddate <= '{endDate}' AND
            requesttype IN ({requestTypes}) AND
            nc IN ({ncList})
        """
    else:
        cdList = (', ').join([str(cd) for cd in cdList])
        return f"""
            createddate >= '{startDate}' AND
            createddate <= '{endDate}' AND
            requesttype IN ({requestTypes}) AND
            cd IN ({cdList})
        """


def query(fields, filters, table=DEFAULT_TABLE):
    if not fields or not filters:
        return {'Error': 'fields and filters are required'}

    if pb.available():
        return pb.query(table, fields, filters)

    fields = (', ').join(fields)
    return pd.read_sql(f"""
        SELECT {fields}
        FROM {table}
        WHERE {filters}
    """, db.engine)


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
