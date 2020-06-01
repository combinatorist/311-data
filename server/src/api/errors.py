from sanic.response import text
from sanic.handlers import ErrorHandler as EH
import requests_async as requests
from json import dumps
from settings import Slack


SLACK_URL = Slack.WEBHOOK_URL


class ErrorHandler(EH):
    def __init__(self):
        super(ErrorHandler, self).__init__()

    async def default(self, request, exception):
        status_code = getattr(exception, 'status_code', 500)
        if status_code == 500:
            await self.send_to_slack(request, exception)
            return text(exception, 500)
        else:
            return super().default(request, exception)

    async def send_to_slack(self, request, exception):
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

ERROR
{str(exception)}
```
        """

        async with requests.Session() as session:
            await session.post(
                SLACK_URL,
                data=dumps({'text': message}),
                headers={'Content-type': 'application/json'})
