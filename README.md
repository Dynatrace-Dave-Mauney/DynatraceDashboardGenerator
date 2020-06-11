# DynatraceDashboardGenerator
The intent of this project is to allow creation of Dynatrace Dashboards based on an Excel
Spreadsheet that can be modified to produce a variety of simple dashboards based on the full set of metrics available in the environment.

See the spreadsheet (Dashboards workbook, "name" column) for a list of all the dashboards.

Currently, the main focus is on "custom chart" metrics.

Line charts are the default, but Pie, Top List and Single view should work as well, after modification to the "Tiles" worksheet "tileType" column.<br />  

There is an "Overview" dashboard created as well, and it has markdown tile links to various detail dashboards.  Currently, the link to the "Databases" detail dashboard is broken because the "Databases" dashboard is too complex to automate.  You can grab the "Databases" dashboard from https://github.com/Dynatrace-Dave-Mauney/DashboardTemplates if you want to make this work before it is fixed in a future release.<br />  

You can control which dashboards are created by either deleting a row from the "Dashboards" worksheet, or better, by setting the "process" column to "false".

tileTypes Currently Supported:<br /> 
MARKDOWN<br /> 
HOSTS<br /> 
SERVICES<br /> 
APPLICATIONS<br /> 
DATABASES_OVERVIEW<br /> 
SYNTHETIC_TESTS<br />  
<br /> 
HEADER should also work, but I haven't tested it yet.<br />  

These dashboards are "generic" -- they are not limited to specific entities and work well with Management Zones.<br />

Notes: <br />
You will want to modify the owner to your email address or a customer email address.<br />

Use "perform_entire_process.py" to run the whole generation process.<br />

Always use PUT rather than POST for uploading the dashboards as the IDs are designed to remain static and PUT allows that.  This is handled automatically, if you use the supplied "put_all_dashboards_util.py" module to upload dashboards.<br />

See https://github.com/Dynatrace-Dave-Mauney/Snippets for Python modules to assist with downloading dashboards (or other configuration entities) and so forth.
<br />
