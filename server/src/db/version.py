from .conn import exec_sql


def version():
    '''
    returns:
        -1 ==> if metadata table doesn't exist
         0 ==> if metadata table doesn't include 'version'
       > 0 ==> the version in the metadata table
    '''
    try:
        meta = exec_sql('SELECT * FROM metadata LIMIT 1').first()
    except Exception as e:
        return -1
    else:
        if not hasattr(meta, 'version'):
            return 0
        else:
            return meta.version
