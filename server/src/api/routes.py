from sanic.response import json
from datetime import datetime
from multiprocessing import cpu_count

import utils.resource as resource
from settings import Version, Github
import db

from .services import data as data_svc
from .services import visualizations as vis_svc
from .services import comparison as comp_svc
from .services import github as github_svc
from .services import map as map_svc


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
    args = request.json
    filters = {
        'startDate': args.get('startDate', None),
        'endDate': args.get('endDate', None),
        'requestTypes': args.get('requestTypes', []),
        'ncList': args.get('ncList', [])
    }
    zoom = int(args.get('zoom', 0))
    bounds = args.get('bounds', {})
    options = args.get('options', {})

    data = await map_svc.clusters(filters, zoom, bounds, options)
    return json(data)


async def heatmap(request):
    args = request.json
    filters = {
        'startDate': args.get('startDate', None),
        'endDate': args.get('endDate', None),
        'requestTypes': args.get('requestTypes', []),
        'ncList': args.get('ncList', [])
    }

    data = await map_svc.heatmap(filters)
    return json(data)


async def visualizations(request):
    args = request.json
    start = args.get('startDate', None)
    end = args.get('endDate', None)
    ncs = args.get('ncList', [])
    requests = args.get('requestTypes', [])

    data = await vis_svc.visualizations(startDate=start,
                                        endDate=end,
                                        requestTypes=requests,
                                        ncList=ncs)
    return json(data)


async def comparison(request, type):
    args = request.json
    startDate = args.get('startDate', None)
    endDate = args.get('endDate', None)
    requestTypes = args.get('requestTypes', [])
    set1 = args.get('set1', None)
    set2 = args.get('set2', None)

    data = await comp_svc.comparison(type=type,
                                     startDate=startDate,
                                     endDate=endDate,
                                     requestTypes=requestTypes,
                                     set1=set1,
                                     set2=set2)
    return json(data)


async def feedback(request):
    args = request.json
    title = args.get('title', None)
    body = args.get('body', None)

    issue_id = await github_svc.create_issue(title, body)
    response = await github_svc.add_issue_to_project(issue_id)
    return json(response)
