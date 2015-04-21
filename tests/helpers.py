from os import path
from io import open
import httpretty
import sys
import warnings

PY3 = sys.version_info[0] == 3
_cwd = path.dirname(path.abspath(__file__))

def mock_request(*data):
    responses = []
    for page in data:
        with open(path.join(_cwd, 'data', page), 'rb') as f:
            responses.append(httpretty.Response(body=f.read(), status=200))
    httpretty.register_uri(httpretty.GET, 'http://api.wikimapia.org',
                           responses=responses, content_type='application/json',
                           connection='close')

def mock_list_request(function, **opts):
    ext = 'json'
    if 'compression' in opts and opts['compression'] == True:
        ext = 'gz'

    def list_response(request, uri, headers):
        page = '1'
        if 'page' in request.querystring:
            page = request.querystring['page'][0]
        file_name = '{0}.{1:02d}.{2}'.format(function, int(page), ext)
        #print('  LOADING:', file_name)
        body = ''
        with open(path.join(_cwd, 'data', file_name), 'rb') as f:
            body = f.read()
        return (200, headers, body)

    httpretty.register_uri(httpretty.GET, 'http://api.wikimapia.org',
                           body=list_response, content_type='application/json',
                           connection='close')


def without_resource_warnings(func):
    '''
    workaround for Python3 ResourceWarning
    http://stackoverflow.com/a/21500796
    '''
    def wrapper(*args, **kw):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)
            func(*args, **kw)
    return wrapper if PY3 else func
