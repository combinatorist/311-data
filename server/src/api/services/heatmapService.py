import pandas as pd
import hashlib
import json
import cache
from . import data


class HeatmapService(object):
    def pins_key(self, filters):
        filters_json = json.dumps(filters, sort_keys=True).encode('utf-8')
        hashed_json = hashlib.md5(filters_json).hexdigest()
        return 'filters:{}:pins'.format(hashed_json)

    async def get_heatmap(self, filters):
        key = self.pins_key(filters)
        pins = cache.get(key)

        fields = ['latitude', 'longitude']
        if pins is None:
            pins = data.standard_query(fields, filters, table='map')
        else:
            pins = pins[fields]

        return pins.to_numpy()
