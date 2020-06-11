from pandas import DataFrame, read_csv
import pandas as pd

MORE_TILES = "        },"
LAST_TILE  = "        }"

#
# The Dashboard class encapsulates the variables and functions to generate the top and bottom parts of the dashboard JSON.
#
class Dashboard:
    configurationVersions = "1"
    clusterVersion = "1"
    id = "aaaaaaaa-bbbb-cccc-dddd-000000000000"
    name = "Generated Dashboard"
    shared = "false"
    owner = ""
    linkShared = "false"
    published = "false"
    timeframe = ""
    managementZone = "null"
    process = "false"
    width = "5180"
    height = "5180"

    #
    # timeframe and managementZone are passed "as is" for now to get around a pandas "nan" issue (google "pandas null numpy.float64" for example)
    #

    top = '''
{
    "metadata": {
        "configurationVersions": [
            $$configurationVersions$$
        ],
        "clusterVersion": "$$clusterVersion$$"
    },
    "id": "$$id$$",
    "dashboardMetadata": {
        "name": "$$name$$",
        "shared": $$shared$$,
        "owner": "$$owner$$",
        "sharingDetails": {
            "linkShared": $$linkShared$$,
            "published": $$published$$
        },
        "dashboardFilter": {
            "timeframe": "$$timeframe$$",
            "managementZone": $$managementZone$$
        }
    },
    "tiles": ['''

    bottom = '''
    ]
}'''
    def replace(self) :
        self.top = self.top.replace("$$configurationVersions$$", self.configurationVersions)
        self.top = self.top.replace("$$clusterVersion$$", self.clusterVersion)
        self.top = self.top.replace("$$id$$", self.id)
        self.top = self.top.replace("$$name$$", str(self.name))
        self.top = self.top.replace("$$shared$$", str(self.shared))
        self.top = self.top.replace("$$owner$$", str(self.owner))
        self.top = self.top.replace("$$linkShared$$", str(self.linkShared))
        self.top = self.top.replace("$$published$$", self.published)
        self.top = self.top.replace("$$timeframe$$", self.timeframe)
        self.top = self.top.replace("$$managementZone$$", self.managementZone)

    def print_top(self, outfile) :
        print(self.top, file=outfile)

    def print_bottom(self, outfile) :
        print(self.bottom, file=outfile)
#
# The Tile class encapsulates the variables and functions to generate the tiles part of the dashboard JSON.
#
class Tile:
    name = ""
    tileType = "CUSTOM_CHARTING"
    configured = "true"
    top = 0
    left = 0
    width = 304
    height = 304
    timeframe = "null"
    managementZone = "null"
    filterType = "MIXED"
    customName = ""
    defaultName = "Generated Custom Chart"
    legendShown = "true"
    chartType = "TIMESERIES"
    metric = ""
    aggregation = "AVG"
    percentile = "null"
    seriesType = "LINE"
    entityType = "HOST"
    sortAscending = "false"
    sortColumn = "true"
    aggregationRate = "TOTAL"
    dimensionDefinition = ""
    
    template_custom_chart = '''
        {
            "name": "$$name$$",
            "tileType": "$$tileType$$",
            "configured": $$configured$$,
            "bounds": {
                "top": $$top$$,
                "left": $$left$$,
                "width": $$width$$,
                "height": $$height$$
            },
            "tileFilter": {
                "timeframe": $$timeframe$$,
                "managementZone": $$managementZone$$
            },
            "filterConfig": {
                "type": "$$filterType$$",
                "customName": "$$customName$$",
                "defaultName": "$$defaultName$$",
                "chartConfig": {
                    "legendShown": $$legendShown$$,
                    "type": "$$chartType$$",
                    "series": [
                        {
                            "metric": "$$metric$$",
                            "aggregation": "$$aggregation$$",
                            "percentile": $$percentile$$,
                            "type": "$$seriesType$$",
                            "entityType": "$$entityType$$",
                            "dimensions": [
                                {
                                    "id": "0",
                                    "name": "$$dimensionDefinition$$",
                                    "values": [],
                                    "entityDimension": true
                                }
                            ],
                            "sortAscending": $$sortAscending$$,
                            "sortColumn": $$sortColumn$$,
                            "aggregationRate": "$$aggregationRate$$"
                        }
                    ],
                    "resultMetadata": {}
                },
                "filtersPerEntityType": {}
            }'''
    template_header = '''
    {
        "name": "Header",
        "tileType": "HEADER",
        "configured": true,
        "bounds": {
            "top": $$top$$,
            "left": $$left$$,
            "width": $$width$$,
            "height": $$height$$
        },
        "tileFilter": {
            "timeframe": null,
            "managementZone": null
        }'''
    template_markdown = '''
    {
        "name": "Markdown",
        "tileType": "MARKDOWN",
        "configured": true,
        "bounds": {
            "top": $$top$$,
            "left": $$left$$,
            "width": $$width$$,
            "height": $$height$$
        },
        "tileFilter": {
            "timeframe": null,
            "managementZone": null
        },
        "markdown": "$$markdown$$"'''
    template_health = '''
    {
        "name": "$$name$$",
        "tileType": "$$tileType$$",
        "configured": true,
        "bounds": {
            "top": $$top$$,
            "left": $$left$$,
            "width": $$width$$,
            "height": $$height$$
        },
        "tileFilter": {
            "timeframe": null,
            "managementZone": null
        },
        "filterConfig": null,
        "chartVisible": true'''

    HEALTH_NAMES_DICT={'HOSTS': 'Host health',
                       'SERVICES': 'Service health',
                       'APPLICATIONS': 'Application health',
                       'DATABASES_OVERVIEW': 'Database health',
                       'SYNTHETIC_TESTS': 'Synthetic monitor health'
    }

    def replace(self):
        if self.tileType == "CUSTOM_CHARTING":
            self.template_custom_chart = self.template_custom_chart.replace("$$name$$", self.name)
            self.template_custom_chart = self.template_custom_chart.replace("$$tileType$$", self.tileType)
            self.template_custom_chart = self.template_custom_chart.replace("$$configured$$", self.configured)
            self.template_custom_chart = self.template_custom_chart.replace("$$top$$", str(self.top))
            self.template_custom_chart = self.template_custom_chart.replace("$$left$$", str(self.left))
            self.template_custom_chart = self.template_custom_chart.replace("$$width$$", str(self.width))
            self.template_custom_chart = self.template_custom_chart.replace("$$height$$", str(self.height))
            self.template_custom_chart = self.template_custom_chart.replace("$$timeframe$$", self.timeframe)
            self.template_custom_chart = self.template_custom_chart.replace("$$managementZone$$", self.managementZone)
            self.template_custom_chart = self.template_custom_chart.replace("$$filterType$$", self.filterType)
            self.template_custom_chart = self.template_custom_chart.replace("$$customName$$", self.customName)
            self.template_custom_chart = self.template_custom_chart.replace("$$defaultName$$", self.defaultName)
            self.template_custom_chart = self.template_custom_chart.replace("$$legendShown$$", self.legendShown)
            self.template_custom_chart = self.template_custom_chart.replace("$$chartType$$", self.chartType)
            self.template_custom_chart = self.template_custom_chart.replace("$$metric$$", self.metric)
            self.template_custom_chart = self.template_custom_chart.replace("$$aggregation$$", self.aggregation)
            self.template_custom_chart = self.template_custom_chart.replace("$$percentile$$", self.percentile)
            self.template_custom_chart = self.template_custom_chart.replace("$$seriesType$$", self.seriesType)
            self.template_custom_chart = self.template_custom_chart.replace("$$entityType$$", self.entityType)
            self.template_custom_chart = self.template_custom_chart.replace("$$sortAscending$$", self.sortAscending)
            self.template_custom_chart = self.template_custom_chart.replace("$$sortColumn$$", self.sortColumn)
            self.template_custom_chart = self.template_custom_chart.replace("$$aggregationRate$$", self.aggregationRate)
            self.template_custom_chart = self.template_custom_chart.replace("$$dimensionDefinition$$", self.dimensionDefinition)

        if self.tileType in self.HEALTH_NAMES_DICT:
            #print('Replace: Health Type')
            self.name = self.HEALTH_NAMES_DICT[self.tileType]
            self.template_health = self.template_health.replace("$$name$$", self.name)
            self.template_health = self.template_health.replace("$$tileType$$", self.tileType)
            self.template_health = self.template_health.replace("$$top$$", str(self.top))
            self.template_health = self.template_health.replace("$$left$$", str(self.left))
            self.template_health = self.template_health.replace("$$width$$", str(self.width))
            self.template_health = self.template_health.replace("$$height$$", str(self.height))

        if self.tileType == 'MARKDOWN':
            # print('Replace: Markdown')
            self.template_markdown = self.template_markdown.replace("$$markdown$$", self.metric)
            self.template_markdown = self.template_markdown.replace("$$top$$", str(self.top))
            self.template_markdown = self.template_markdown.replace("$$left$$", str(self.left))
            self.template_markdown = self.template_markdown.replace("$$width$$", str(self.width))
            self.template_markdown = self.template_markdown.replace("$$height$$", str(self.height))

        if self.tileType == 'HEADER':
            # print('Replace: Header')
            self.template_header = self.template_header.replace("$$top$$", str(self.top))
            self.template_header = self.template_header.replace("$$left$$", str(self.left))
            self.template_header = self.template_header.replace("$$width$$", str(self.width))
            self.template_header = self.template_header.replace("$$height$$", str(self.height))

    def print(self, outfile) :
        #self.replace()
        if self.tileType == "CUSTOM_CHARTING":
            print(self.template_custom_chart, file=outfile)
        if self.tileType in self.HEALTH_NAMES_DICT:
            #print('Print: Health Type')
            print(self.template_health, file=outfile)
        if self.tileType == "MARKDOWN":
            #print('Print: Markdown')
            print(self.template_markdown, file=outfile)
        if self.tileType == "HEADER":
            #print('Print: Markdown')
            print(self.template_header, file=outfile)

def increment(id):
    last12_digits = id[-12:]
    new_last12_digits = int(last12_digits)+100000000000
    newId = id[0:24] + str(new_last12_digits)
    return newId

def increment_name(name, id):
    suffix = str(int(id[-12]) + 1)
    new_name = name + "-" + suffix
    return new_name

#
# Read the "dashboard_controller.xlsx" file
# For each Dashboard Sheet Row, Find the matching Tile Sheet Rows
# If there are matches, write the dashboard and the matching tiles to JSON dashboard file
#
def generate():
    file = r'dashboard_controller.xlsx'
    dashboards = pd.read_excel(file, sheet_name='Dashboards', na_filter=False)
    tiles = pd.read_excel(file, sheet_name='Tiles', na_filter=False)

    dashboard_rows = len(dashboards)
    dashboard_row = 0
    while dashboard_row < dashboard_rows:
        dashboard = Dashboard()
        dashboard.name = dashboards['name'][dashboard_row]
        dashboard.id = dashboards['id'][dashboard_row]
        dashboard.owner = dashboards['owner'][dashboard_row]
        dashboard.clusterVersion = dashboards['clusterVersion'][dashboard_row]
        dashboard.configurationVersions = dashboards['configurationVersions'][dashboard_row].astype(str)
        dashboard.shared = dashboards['shared'][dashboard_row].astype(str).lower()
        dashboard.linkShared = dashboards['linkShared'][dashboard_row].astype(str).lower()
        dashboard.published = dashboards['published'][dashboard_row].astype(str).lower()
        dashboard.timeframe = dashboards['timeframe'][dashboard_row]
        dashboard.managementZone = dashboards['managementZone'][dashboard_row]
        dashboard.process = dashboards['process'][dashboard_row].astype(str).lower()
        dashboard.width = dashboards['width'][dashboard_row]
        dashboard.height = dashboards['height'][dashboard_row]
        dashboard_row += 1

        if dashboard.process == "false":
            continue

        #print(dashboard.height)

        matching_tiles = tiles[tiles.name.eq(dashboard.name)]
        tile_rows = matching_tiles.last_valid_index()
        tile_row = matching_tiles.first_valid_index()
        if tile_row is None:
            continue

        outfile = open(dashboard.id, "w")
        
        dashboard.replace()
        dashboard.print_top(outfile)
        print("Writing Dashboard: " + dashboard.name + " - " + dashboard.id)

        #print("Matching for " + dashboard.name + ":")
        #matching_tiles = tiles[tiles.name.eq(dashboard.name)]
        #print(matching_tiles)
        #print(matching_tiles.first_valid_index())
        #print(matching_tiles.last_valid_index())
        #tile_rows = matching_tiles.last_valid_index()
        #tile_row = matching_tiles.first_valid_index()
        tile_printed = False
        top = 0
        left = 0
        #width = 304
        #height = 304

        while tile_row <= tile_rows:
            if tile_printed :
                print(MORE_TILES, file=outfile)

            tile = Tile()
            tile.tileType = matching_tiles['tileType'][tile_row]
            tile.metric = matching_tiles['metric'][tile_row]
            tile.customName = matching_tiles['customName'][tile_row]
            tile.aggregation = matching_tiles['aggregation'][tile_row]
            tile.chartType = matching_tiles['type'][tile_row]
            tile.filterType = matching_tiles['filterType'][tile_row]
            tile.entityType = matching_tiles['entityType'][tile_row]
            tile.dimensionDefinition = matching_tiles['dimensionDefinition'][tile_row]
            tile.width = matching_tiles['width'][tile_row]
            tile.height = matching_tiles['height'][tile_row]
            width = int(tile.width)
            height = int(tile.height)

            tile.top = top
            tile.left = left
            tile.replace()
            tile.print(outfile)
            tile_row += 1
            tile_printed = True

            # print(str(top) + "/" + str(left))
            # print(dashboard.width)
            # print(width)
            left = left + width
            if left > (dashboard.width - width):
                #print(str(left) + ">" + str(dashboard.width - width))
                left = 0
                top = top + height
                if top > (dashboard.height - height):
                    #print(str(top) + ">" + str(dashboard.height - height))
                    #print("Dashboard height exceeds maximum.  Either increase width, height, reduce number of tiles or split into multiple dashboards.")
                    #finish up this dashboard and start a new one with an id incremented by one
                    #finishing up here
                    print(LAST_TILE, file=outfile)
                    dashboard.print_bottom(outfile)
                    #starting next dashboard here
                    left = 0
                    top = 0
                    tile_printed = False
                    new_id = increment(dashboard.id)
                    new_name = increment_name(dashboard.name, new_id)
                    dashboard.top = dashboard.top.replace(dashboard.id, new_id)
                    dashboard.top = dashboard.top.replace(dashboard.name, new_name)
                    dashboard.id = new_id
                    print("Writing Dashboard: " + new_name + " - " + dashboard.id + " (Continuation)")
                    #print(dashboard.top)
                    #print(dashboard.id + "->" + new_id)
                    #print(dashboard.top)
                    outfile = open(dashboard.id, "w")
                    dashboard.print_top(outfile)
                    continue

        print(LAST_TILE, file=outfile)
            
        dashboard.print_bottom(outfile)
    
def main():
    generate()

if __name__ == '__main__':
	main()    
