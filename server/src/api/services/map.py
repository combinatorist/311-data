import pysupercluster
import hashlib
import json
import cache
from . import data


def pins_key(filters):
    filters_json = json.dumps(filters, sort_keys=True).encode('utf-8')
    hashed_json = hashlib.md5(filters_json).hexdigest()
    return 'filters:{}:pins'.format(hashed_json)


def get_pins(filters):
    key = pins_key(filters)
    pins = cache.get(key)

    if pins is None:
        pins = data.standard_query([
            'srnumber',
            'requesttype',
            'latitude',
            'longitude'
        ], filters, table='map')

        cache.set(key, pins)

    return pins


def get_clusters(pins, zoom, bounds, options={}):
    if len(pins) == 0:
        return []

    min_zoom = options.get('min_zoom', 0)
    max_zoom = options.get('max_zoom', 17)
    radius = options.get('radius', 200)
    extent = options.get('extent', 512)

    index = pysupercluster.SuperCluster(
        pins[['longitude', 'latitude']].to_numpy(),
        min_zoom=min_zoom,
        max_zoom=max_zoom,
        radius=radius,
        extent=extent)

    north = bounds.get('north', 90)
    south = bounds.get('south', -90)
    west = bounds.get('west', -180)
    east = bounds.get('east', 180)

    clusters = index.getClusters(
        top_left=(west, north),
        bottom_right=(east, south),
        zoom=zoom)

    for cluster in clusters:
        if cluster['count'] == 1:
            pin = pins.iloc[cluster['id']]
            cluster['srnumber'] = pin['srnumber']
            cluster['requesttype'] = pin['requesttype']
            del cluster['expansion_zoom']

    return clusters


async def clusters(filters, zoom, bounds, options):
    pins = get_pins(filters)
    return get_clusters(pins, zoom, bounds, options)


async def heatmap(filters):
    key = pins_key(filters)
    pins = cache.get(key)

    fields = ['latitude', 'longitude']
    if pins is None:
        pins = data.standard_query(fields, filters, table='map')
    else:
        pins = pins[fields]

    return pins.to_numpy()
