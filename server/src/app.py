from sanic import Sanic
from sanic_cors import CORS
from sanic_compress import Compress
from multiprocessing import cpu_count
import api.routes as R
from api.errors import ErrorHandler
from api.headers import add_performance_header
from utils.log import log_heading
from settings import Server


app = Sanic(__name__)


routes = {
    '/': (
        ['GET'], R.index),

    '/apistatus': (
        ['GET', 'HEAD'], R.apistatus),

    '/database': (
        ['GET'], R.database),

    '/system': (
        ['GET'], R.system),

    '/servicerequest/<srnumber>': (
        ['GET'], R.request_detail),

    '/pin-clusters': (
        ['POST'], R.pin_clusters),

    '/heatmap': (
        ['POST'], R.heatmap),

    '/visualizations': (
        ['POST'], R.visualizations),

    '/comparison/<type>': (
        ['POST'], R.comparison),

    '/feedback': (
        ['POST'], R.feedback)}


if __name__ == '__main__':
    log_heading('starting server')

    CORS(app)
    Compress(app)

    for route, (methods, handler) in routes.items():
        app.add_route(handler, route, methods)

    app.error_handler = ErrorHandler()

    if Server.DEBUG:
        add_performance_header(app)

    workers = Server.WORKERS
    if workers == -1:
        workers = max(cpu_count() // 2, 1)

    app.run(
        port=Server.PORT,
        host=Server.HOST,
        debug=Server.DEBUG,
        workers=workers)
