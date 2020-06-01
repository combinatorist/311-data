from . import data
from utils.stats import box_plots, date_bins, date_histograms, counts


class VisualizationsService(object):
    async def visualizations(self,
                             startDate=None,
                             endDate=None,
                             requestTypes=[],
                             ncList=[]):

        bins, start, end = date_bins(startDate, endDate)

        fields = [
            'requesttype',
            'createddate',
            '_daystoclose',
            'requestsource']

        filters = data.standardFilters(
            start, end, requestTypes, ncList)

        df = data.query(fields, filters, table='vis')

        inner_df = df.loc[
            (df['createddate'] >= startDate) &
            (df['createddate'] <= endDate)]

        return {
            'frequency': {
                'bins': list(bins.astype(str)),
                'counts': date_histograms(
                    df,
                    dateField='createddate',
                    bins=bins,
                    groupField='requesttype',
                    groupFieldItems=requestTypes)
            },

            'timeToClose': box_plots(
                inner_df,
                plotField='_daystoclose',
                groupField='requesttype',
                groupFieldItems=requestTypes),

            'counts': {
                'type': counts(inner_df, groupField='requesttype'),
                'source': counts(inner_df, groupField='requestsource')
            }
        }
