import sys
import create_metrics_and_version_files
import generate_dashboard_controller
import generate_dashboards_from_spreadsheet
import put_all_dashboards_util

def main(arguments):
    # Create new "metrics.txt" and "version.txt" files used to drive the dashboard generation process
    # for a specific cluster/tenant version
    create_metrics_and_version_files.main(arguments)

    # Generate the spreadsheet used to control what dashboards and tiles are generated
    # CAUTION: This module will currently OVERWRITE the output file, so if you plan to modify the spreadsheet, always make a copy for that
    generate_dashboard_controller.main()

    # Modify the Dashboard Controller Spreadsheet manually, if needed...
    # Comment the "input" line if no manual changes are needed
    # Optionally add your own customization process here to automate the modification process
    #input('Modify the Dashboard Controller Spreadsheet, If Needed, and Then Press Enter to Continue...')

    # Generate the dashboards from the dashboard JSON files from the Dashboard Controller Spreadsheet
    generate_dashboards_from_spreadsheet.main()

    # Add or update all the generated dashboards on a cluster/tenant
    # All dashboards with the expected file name pattern in the current directory will be processed
    put_all_dashboards_util.main(arguments)

if __name__ == '__main__':
    main(sys.argv)

