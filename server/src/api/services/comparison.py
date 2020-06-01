from . import data
from .stats import box_plots, date_bins, date_histograms, counts


def frequency_comparison(startDate=None,
                         endDate=None,
                         requestTypes=[],
                         set1={'district': None, 'list': []},
                         set2={'district': None, 'list': []}):

    def get_data(district, items, bins, start, end):
        filters = {
            'startDate': start,
            'endDate': end,
            'requestTypes': requestTypes
        }

        if district == 'nc':
            filters['ncList'] = items
            groupField = 'nc'
        elif district == 'cc':
            filters['cdList'] = items
            groupField = 'cd'

        fields = [groupField, 'createddate']
        df = data.comparison_query(fields, filters, table='vis')

        return date_histograms(
            df,
            dateField='createddate',
            bins=bins,
            groupField=groupField,
            groupFieldItems=items)

    bins, start, end = date_bins(startDate, endDate)
    set1data = get_data(set1['district'], set1['list'], bins, start, end)
    set2data = get_data(set2['district'], set2['list'], bins, start, end)

    return {
        'bins': list(bins.astype(str)),
        'set1': {
            'district': set1['district'],
            'counts': set1data
        },
        'set2': {
            'district': set2['district'],
            'counts': set2data
        }
    }


def ttc_comparison(startDate=None,
                   endDate=None,
                   requestTypes=[],
                   set1={'district': None, 'list': []},
                   set2={'district': None, 'list': []}):

    def get_data(district, items):
        filters = {
            'startDate': startDate,
            'endDate': endDate,
            'requestTypes': requestTypes
        }

        if district == 'nc':
            filters['ncList'] = items
            groupField = 'nc'
        elif district == 'cc':
            filters['cdList'] = items
            groupField = 'cd'

        fields = [groupField, '_daystoclose']
        df = data.comparison_query(fields, filters, table='vis')

        return box_plots(
            df,
            plotField='_daystoclose',
            groupField=groupField,
            groupFieldItems=items)

    set1data = get_data(set1['district'], set1['list'])
    set2data = get_data(set2['district'], set2['list'])

    return {
        'set1': {
            'district': set1['district'],
            'data': set1data
        },
        'set2': {
            'district': set2['district'],
            'data': set2data
        }
    }


def counts_comparison(startDate=None,
                      endDate=None,
                      requestTypes=[],
                      set1={'district': None, 'list': []},
                      set2={'district': None, 'list': []}):

    def get_data(district, items):
        filters = {
            'startDate': startDate,
            'endDate': endDate,
            'requestTypes': requestTypes
        }

        if district == 'nc':
            filters['ncList'] = items
        elif district == 'cc':
            filters['cdList'] = items

        fields = ['requestsource']
        df = data.comparison_query(fields, filters, table='vis')

        return counts(df, 'requestsource')

    set1data = get_data(set1['district'], set1['list'])
    set2data = get_data(set2['district'], set2['list'])

    return {
        'set1': {
            'district': set1['district'],
            'source': set1data
        },
        'set2': {
            'district': set2['district'],
            'source': set2data
        }
    }


async def comparison(type=None,
                     startDate=None,
                     endDate=None,
                     requestTypes=[],
                     set1={'district': None, 'list': []},
                     set2={'district': None, 'list': []}):

    args = {
        'startDate': startDate,
        'endDate': endDate,
        'requestTypes': requestTypes,
        'set1': set1,
        'set2': set2}

    if type == 'frequency':
        return frequency_comparison(**args)
    elif type == 'timetoclose':
        return ttc_comparison(**args)
    elif type == 'counts':
        return counts_comparison(**args)
    else:
        return {'Error': 'Unrecognized comparison type'}
