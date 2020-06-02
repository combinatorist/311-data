from sanic.response import json
from .services import (
    data as data_svc,
    visualizations as vis_svc,
    comparison as comp_svc,
    github as github_svc,
    map as map_svc,
    status as status_svc)
from .errors import to


async def index(request):
    return json('You hit the index')


async def apistatus(request):
    data = await status_svc.api()
    return json(data)


async def system(request):
    data = await status_svc.system()
    return json(data)


async def database(request):
    data = await status_svc.database()
    return json(data)


async def requestDetails(request, srnumber):
    data = data_svc.item_query(srnumber)
    return json(data)


async def pinClusters(request):
    args = request.json

    startDate = args.get('startDate', None)
    endDate = args.get('endDate', None)
    requestTypes = args.get('requestTypes', [])
    ncList = args.get('ncList', [])
    zoom = int(args.get('zoom', 0))
    bounds = args.get('bounds', {})
    options = args.get('options', {})

    data = await map_svc.clusters(startDate=startDate,
                                  endDate=endDate,
                                  requestTypes=requestTypes,
                                  ncList=ncList,
                                  zoom=zoom,
                                  bounds=bounds,
                                  options=options)
    return json(data)


async def heatmap(request):
    data = await map_svc.heatmap(**to.unpack(request.json, {
        'startDate': to.req.DATE,
        'endDate': to.req.DATE,
        'requestTypes': to.opt.LIST_OF_STR,
        'ncList': to.opt.LIST_OF_INT
    }))

    return json(data)


async def visualizations(request):
    data = await vis_svc.visualizations(**to.unpack(request.json, {
        'startDate': to.req.DATE,
        'endDate': to.req.DATE,
        'requestTypes': to.opt.LIST_OF_STR,
        'ncList': to.opt.LIST_OF_INT
    }))

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
