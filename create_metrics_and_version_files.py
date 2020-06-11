#
# Access the metrics v2 API and gather all metrics along with their details using "fields" parameter:
# fields=fields=+displayName,+description,+unit,+aggregationTypes,+defaultAggregation,+dimensionDefinitions,+transformations,+entityType
#
# The primary use case for this file is as input to the "generate_dashboard_controller.py" module, in order to create a spreadsheet used to control the creation of dashboards.
#

import pathlib, requests, sys


def get_version(url, token):
    versionEndpoint = '/api/v1/config/clusterversion'
    fullURL = url + versionEndpoint
    myheaders = {'Authorization': "Api-Token " + token}
    resp = requests.get(fullURL, headers=myheaders)
    if resp.status_code != 200:
        print('GET ' + fullURL + ' {}'.format(resp.status_code))
        exit()
    version: str = resp.json().get("version", "?")
    return version


def process(arguments):
    # Assume tenant/environment URL followed by Token
    url = arguments[1]
    token = arguments[2]

    print('url: ' + url)
    print('token: ' + token[0:4] + '******************' + ' (masked for security)')

    version = get_version(url, token)

    file = pathlib.Path('version.txt')
    outfile = open(str(file), 'w')
    print(version, file=outfile)

    print('version: ' + version + ' written to ' + outfile.name)

    file = pathlib.Path('metrics.txt')
    #It's inexpensive to recreate the metrics data, so let it overwrite by default.
    #if file.exists():
    #    print('The output file named "' + str(
    #        file) + '" already exists.  Please delete or rename it and run this module again if you really want to recreate the file.')
    #    exit(1)

    outfile = open(str(file), 'w')

    endpoint = '/api/v2/metrics'
    params = '?pageSize=1000&fields=+displayName,+description,+unit,+aggregationTypes,+defaultAggregation,+dimensionDefinitions,+transformations,+entityType'
    fullURL = url + endpoint + params
    HEADERS = {'Authorization': "Api-Token " + token}

    resp = requests.get(fullURL, headers=HEADERS)
    if resp.status_code != 200:
        print('GET ' + fullURL + ' {}'.format(resp.status_code))
        exit()

    dict = resp.json()
    metrics = dict.get('metrics')
    nextPageKey = dict.get('nextPageKey')

    while nextPageKey != None:
        params = '?nextPageKey=' + nextPageKey
        fullURL = url + endpoint + params
        resp = requests.get(fullURL, headers=HEADERS)

        if resp.status_code != 200:
            print('GET ' + fullURL + ' {}'.format(resp.status_code))
            exit()

        dictPaged = resp.json()
        metricsPaged = dictPaged.get('metrics')
        nextPageKey = dictPaged.get('nextPageKey')
        metrics.extend(metricsPaged)

    metricsWritten = 0

    for metricDict in metrics:
        print(metricDict, file=outfile)
        metricsWritten += 1

    print(str(metricsWritten) + ' metrics were written to ' + outfile.name)


def main(arguments):
    help = '''
    create_metrics_with_details_file downloads the Metrics from the specified tenant/environment if the file does not yet exist for the current Dynatrace version.

    Usage:    create_metrics_and_version_files.py <tenant/environment URL> <token>
    Examples: create_metrics_and_version_files.py https://TENANTID.live.dynatrace.com ABCD123ABCD123
              create_metrics_and_version_files.py https://TENANTID.dynatrace-managed.com/e/aaaaaaaa-bbbb-cccc-dddd-cccccccccccc ABCD123ABCD123
    '''

    print('args' + str(arguments))
    if len(arguments) < 2:
        print(help)
        raise ValueError('Too few arguments!')
    if len(arguments) > 3:
        print(help)
        raise ValueError('Too many arguments!')
    if arguments[1] in ['-h', '--help']:
        print(help)
    elif arguments[1] in ['-v', '--version']:
        print('1.0')
    else:
        if len(arguments) == 3:
            process(arguments)
        else:
            print(help)
            raise ValueError('Incorrect arguments!')


if __name__ == '__main__':
    main(sys.argv)
