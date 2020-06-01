from . import data


class RequestDetailService(object):
    async def get_request_detail(self, requestNumber=None):
        return data.item_query(requestNumber)
