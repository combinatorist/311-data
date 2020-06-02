import traceback
from json import dumps
import pandas as pd
import requests_async as requests
from sanic.response import text
from sanic.handlers import ErrorHandler as EH
from sanic.exceptions import ServerError
from settings import Slack
from utils.log import log, log_colors


SLACK_URL = Slack.WEBHOOK_URL
ERROR_CODES = Slack.ERROR_CODES


class ErrorHandler(EH):
    def __init__(self):
        super(ErrorHandler, self).__init__()

    async def default(self, request, exception):
        status_code = getattr(exception, 'status_code', 500)
        trace = traceback.format_exc()

        if status_code in ERROR_CODES:
            await self.send_to_slack(request, trace, status_code)

        if status_code == 400:
            log(f'400 ERROR: {exception}', color=log_colors.WARNING)
            return text(exception, status_code)
        elif status_code == 500:
            log(trace, color=log_colors.FAIL)
            return text(trace, status_code)
        else:
            return super().default(request, exception)

    async def send_to_slack(self, request, trace, status_code):
        if SLACK_URL is None:
            return

        if (request.query_string == ''):
            qs = ''
        else:
            qs = '?{}'.format(request.query_string)

        if request.json is None:
            params = ''
        else:
            params = '\n{}'.format(dumps(request.json, indent=2))

        message = f"""
```
{request.method} {request.path}{qs} {params}

{status_code} ERROR
{trace}```
        """

        async with requests.Session() as session:
            await session.post(
                SLACK_URL,
                data=dumps({'text': message}),
                headers={'Content-type': 'application/json'})


class to:
    class opt:
        INT = 'INT'
        LIST_OF_INT = 'LIST_OF_INT'
        LIST_OF_STR = 'LIST_OF_STR'
        DICT_OF_INT = 'DICT_OF_INT'
        DICT_OF_FLOAT = 'DICT_OF_FLOAT'

    class req:
        STR = 'STR'
        DATE = 'DATE'
        COMPARISON_SET = 'COMPARISON_SET'

    def error(message, code=400):
        raise ServerError(message, status_code=code)

    def parse_arg(value, to_type):
        if to_type == to.opt.INT:
            return int(value)

        elif to_type == to.opt.LIST_OF_INT:
            return [int(item) for item in value]

        elif to_type == to.opt.LIST_OF_STR:
            return [str(item) for item in value]

        elif to_type == to.opt.DICT_OF_INT:
            return {key: int(val) for key, val in value.items()}

        elif to_type == to.opt.DICT_OF_FLOAT:
            return {key: float(val) for key, val in value.items()}

        elif to_type == to.req.STR:
            return str(value)

        elif to_type == to.req.DATE:
            return pd.to_datetime(value)

        elif to_type == to.req.COMPARISON_SET:
            if value.get('district') not in ['nc', 'cc']:
                raise Exception('district must be either "nc" or "cc".')

            return {
                'district': value['district'],
                'list': [int(item) for item in value['list']]}

    def parse(args, expected_args, to_camel=False):
        out = {}

        for expected, to_type in expected_args.items():
            if expected not in args:
                if hasattr(to.req, to_type):
                    to.error(f'{expected} is required.')
                else:
                    continue
            try:
                out[expected] = to.parse_arg(args[expected], to_type)
            except Exception:
                to.error(f'{expected} could not be parsed to {to_type}.')

        return out
