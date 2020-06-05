# DynatraceDashboardGenerator
The intent of this project is to allow creation of Dynatrace Dashboards based on an Excel
Spreadsheet that can be modified to produce a variety of simple dashboards based on the full set of metrics available in the environment.

See the spreadsheet (Dashboards workbook, "name" column) for a list of all the dashboards.

Currently, the main focus is on "custom chart" metrics.

Line charts are the default, but Pie, Top List and Single view should work as well, after modification to the "Tiles" worksheet "tileType" column.<br />  

There is an "Overview" dashboard created as well, that has links to itself only by default and requires the user to modify the links to point to the destination dashboards.
This will be automated in a future release.<br />  

You can control which dashboards are created by either deleting a row from the "Dashboards" worksheet, or better, by setting the "process" column to "false".

tileTypes Currently Supported:
MARKDOWN
HOSTS
SERVICES
APPLICATIONS
DATABASES_OVERVIEW
SYNTHETIC_TESTS<br />  

HEADER should also work, but I haven't tried it yet.
<br />  

These dashboards are "generic" -- they are not limited to specific entities and work well with Management Zones.<br />

Notes: <br />
The Overview dashboard provides drilldowns to child dashboards via markdown tiles.<br />
You might want to modify the owner to your email address or a customer email address.<br />
Version differences can be an issue, so select the most recent version equal or prior to the version of the cluster/tenant you are importing into.<br />
Always use PUT rather than POST as the IDs are designed to remain static and PUT allows that.<br />

See my "Snippets" repo for Python modules to assist with pushing dashboards, saving dashboards (or other configuration entities) and so forth.<br />
