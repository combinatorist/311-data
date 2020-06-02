from sanic.response import json
from .errors import to
from .services import (
    data as data_svc,
    visualizations as vis_svc,
    comparison as comp_svc,
    github as github_svc,
    map as map_svc,
    status as status_svc)


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
    data = await map_svc.clusters(**to.parse(request.json, {
        'startDate': to.req.DATE,
        'endDate': to.req.DATE,
        'requestTypes': to.opt.LIST_OF_STR,
        'ncList': to.opt.LIST_OF_INT,
        'zoom': to.opt.INT,
        'bounds': to.opt.DICT_OF_INT,
        'options': to.opt.DICT_OF_INT}))

    return json(data)


async def heatmap(request):
    data = await map_svc.heatmap(**to.parse(request.json, {
        'startDate': to.req.DATE,
        'endDate': to.req.DATE,
        'requestTypes': to.opt.LIST_OF_STR,
        'ncList': to.opt.LIST_OF_INT}))

    return json(data)


async def visualizations(request):
    data = await vis_svc.visualizations(**to.parse(request.json, {
        'startDate': to.req.DATE,
        'endDate': to.req.DATE,
        'requestTypes': to.opt.LIST_OF_STR,
        'ncList': to.opt.LIST_OF_INT}))

    return json(data)


async def comparison(request, type):
    data = await comp_svc.comparison(type, **to.parse(request.json, {
        'startDate': to.req.DATE,
        'endDate': to.req.DATE,
        'requestTypes': to.opt.LIST_OF_STR,
        'set1': to.req.COMPARISON_SET,
        'set2': to.req.COMPARISON_SET}))

    return json(data)


async def feedback(request):
    args = to.parse(request.json, {
        'title': to.req.STR,
        'body': to.req.STR})

    issue_id = await github_svc.create_issue(args['title'], args['body'])
    response = await github_svc.add_issue_to_project(issue_id)

    return json(response)
