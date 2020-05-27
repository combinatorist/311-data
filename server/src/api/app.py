from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from sanic_compress import Compress
from datetime import datetime
from multiprocessing import cpu_count

from .services.pinClusterService import PinClusterService
from .services.heatmapService import HeatmapService
from .services.requestDetailService import RequestDetailService
from .services.visualizationsService import VisualizationsService
from .services.comparisonService import ComparisonService
from .services.feedbackService import FeedbackService

from utils.sanic import add_performance_header
import utils.resource as resource
from settings import Version, Github, Server
import db

app = Sanic(__name__)
CORS(app)
Compress(app)


@app.route('/')
async def index(request):
    return json('You hit the index')


@app.route('/apistatus', methods=["GET", "HEAD"])
async def healthcheck(request):
    currentTime = datetime.utcnow().replace(microsecond=0)
    semVersion = '{}.{}.{}'.format(Version.MAJOR, Version.MINOR, Version.PATCH)

    return json({
        'currentTime': f'{currentTime.isoformat()}Z',
        'gitSha': Github.SHA,
        'version': semVersion,
        'lastPulled': f'{db.info.last_updated().isoformat()}Z'})


@app.route('/system')
async def system(request):
    return json({
        'cpuCount': cpu_count(),
        'pageSize': resource.page_size(),
        'limits': resource.limits(),
        'usage': resource.usage()})


@app.route('/database')
async def database(request):
    return json({
        'tables': db.info.tables(),
        'rows': db.info.rows()})


@app.route('/pin-clusters', methods=["POST"])
async def pinClusters(request):
    worker = PinClusterService()

    postArgs = request.json
    filters = {
        'startDate': postArgs.get('startDate', None),
        'endDate': postArgs.get('endDate', None),
        'requestTypes': postArgs.get('requestTypes', []),
        'ncList': postArgs.get('ncList', [])
    }
    zoom = int(postArgs.get('zoom', 0))
    bounds = postArgs.get('bounds', {})
    options = postArgs.get('options', {})

    clusters = await worker.get_pin_clusters(filters, zoom, bounds, options)
    return json(clusters)


@app.route('/heatmap', methods=["POST"])
async def heatmap(request):
    worker = HeatmapService()

    postArgs = request.json
    filters = {
        'startDate': postArgs.get('startDate', None),
        'endDate': postArgs.get('endDate', None),
        'requestTypes': postArgs.get('requestTypes', []),
        'ncList': postArgs.get('ncList', [])
    }

    heatmap = await worker.get_heatmap(filters)
    return json(heatmap)


@app.route('/servicerequest/<srnumber>', methods=["GET"])
async def requestDetails(request, srnumber):
    detail_worker = RequestDetailService()

    return_data = await detail_worker.get_request_detail(srnumber)
    return json(return_data)


@app.route('/visualizations', methods=["POST"])
async def visualizations(request):
    worker = VisualizationsService()

    postArgs = request.json
    start = postArgs.get('startDate', None)
    end = postArgs.get('endDate', None)
    ncs = postArgs.get('ncList', [])
    requests = postArgs.get('requestTypes', [])

    data = await worker.visualizations(startDate=start,
                                       endDate=end,
                                       requestTypes=requests,
                                       ncList=ncs)
    return json(data)


@app.route('/comparison/<type>', methods=["POST"])
async def comparison(request, type):
    worker = ComparisonService()

    postArgs = request.json
    startDate = postArgs.get('startDate', None)
    endDate = postArgs.get('endDate', None)
    requestTypes = postArgs.get('requestTypes', [])
    set1 = postArgs.get('set1', None)
    set2 = postArgs.get('set2', None)

    data = await worker.comparison(type=type,
                                   startDate=startDate,
                                   endDate=endDate,
                                   requestTypes=requestTypes,
                                   set1=set1,
                                   set2=set2)
    return json(data)


@app.route('/feedback', methods=["POST"])
async def handle_feedback(request):
    github_worker = FeedbackService()
    postArgs = request.json
    title = postArgs.get('title', None)
    body = postArgs.get('body', None)

    issue_id = await github_worker.create_issue(title, body)
    response = await github_worker.add_issue_to_project(issue_id)
    return json(response)


def start():
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


def stop():
    print('stopping api')
    app.stop()
