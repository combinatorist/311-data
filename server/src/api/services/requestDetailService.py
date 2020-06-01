from . import dataAccess


class RequestDetailService(object):
    async def get_request_detail(self, requestNumber=None):
        return dataAccess.itemQuery(requestNumber)
