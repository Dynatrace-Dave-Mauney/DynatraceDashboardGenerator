# Put all dashboards in the current directory to tenant/environment specified via command line argument.
#
# CAUTION:
#
# The file name is assumed to be the dashboard id.
# All files in the current directory with the following format will be assumed to be dashboards:
# ????????-????-????-????-????????????
# Example:
# aaaaaaaa-bbbb-cccc-dddd-000000000001
#

import requests, ssl, os, sys, glob

def putDashboard(env, token, id, payload):
        HEADERS = {'Authorization': 'Api-Token ' + token, 'Content-Type': 'application/json; charset=utf-8'}
        url = env + '/api/config/v1/dashboards/' + id
        print('PUT: ' + url)
        try:
                r = requests.put(url, payload, headers=HEADERS)
                # If you need to bypass certificate checks on managed and are ok with the risk:
                #r = requests.put(url, payload, headers=HEADERS, verify=False)
                print('Status Code: %d' % (r.status_code))
                if len(r.text) > 0: print(r.text)
        except ssl.SSLError:
                print('SSL Error')

def putDashboards(env, token):
        path='./????????-????-????-????-????????????'
        for filename in glob.glob(path):
            with open(filename, 'r') as f:
                putDashboard(env, token, os.path.basename(f.name), f.read())

def main(arguments):
    help = '''
    put_all_dashboards.py: Put all dashboards in the current directory to tenant/environment specified via command line argument.

    Usage:    put_all_dashboards.py <tenant/environment URL> <token>
    Examples: put_all_dashboards.py https://TENANTID.live.dynatrace.com ABCD123ABCD123
              put_all_dashboards.py https://TENANTID.dynatrace-managed.com/e/aaaaaaaa-bbbb-cccc-dddd-cccccccccccc ABCD123ABCD123
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
            putDashboards(arguments[1], arguments[2])
        else:
            print(help)
            raise ValueError('Incorrect arguments!')

if __name__ == '__main__':
    main(sys.argv)
