from sanic.response import json
from datetime import datetime
from multiprocessing import cpu_count

from .services.pinClusterService import PinClusterService
from .services.heatmapService import HeatmapService
from .services.feedbackService import FeedbackService

import utils.resource as resource
from settings import Version, Github
import db

from .services import data as data_svc
from .services import visualizations as vis_svc
from .services import comparison as comp_svc


async def index(request):
    return json('You hit the index')


async def apistatus(request):
    currentTime = datetime.utcnow().replace(microsecond=0)
    semVersion = '{}.{}.{}'.format(Version.MAJOR, Version.MINOR, Version.PATCH)

    return json({
        'currentTime': f'{currentTime.isoformat()}Z',
        'gitSha': Github.SHA,
        'version': semVersion,
        'lastPulled': f'{db.info.last_updated().isoformat()}Z'})


async def system(request):
    return json({
        'cpuCount': cpu_count(),
        'pageSize': resource.page_size(),
        'limits': resource.limits(),
        'usage': resource.usage()})


async def database(request):
    return json({
        'tables': db.info.tables(),
        'rows': db.info.rows()})


async def requestDetails(request, srnumber):
    data = data_svc.item_query(srnumber)
    return json(data)


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


async def visualizations(request):
    postArgs = request.json
    start = postArgs.get('startDate', None)
    end = postArgs.get('endDate', None)
    ncs = postArgs.get('ncList', [])
    requests = postArgs.get('requestTypes', [])

    data = await vis_svc.visualizations(startDate=start,
                                        endDate=end,
                                        requestTypes=requests,
                                        ncList=ncs)
    return json(data)


async def comparison(request, type):
    postArgs = request.json
    startDate = postArgs.get('startDate', None)
    endDate = postArgs.get('endDate', None)
    requestTypes = postArgs.get('requestTypes', [])
    set1 = postArgs.get('set1', None)
    set2 = postArgs.get('set2', None)

    data = await comp_svc.comparison(type=type,
                                     startDate=startDate,
                                     endDate=endDate,
                                     requestTypes=requestTypes,
                                     set1=set1,
                                     set2=set2)
    return json(data)


async def feedback(request):
    github_worker = FeedbackService()
    postArgs = request.json
    title = postArgs.get('title', None)
    body = postArgs.get('body', None)

    issue_id = await github_worker.create_issue(title, body)
    response = await github_worker.add_issue_to_project(issue_id)
    return json(response)
