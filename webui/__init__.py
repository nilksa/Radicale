import os

from bottle import get, post, run, static_file
from bottlehaml import haml_template
from radicale import storage
from radicale.ical import unfold

module_path = lambda rpath: os.path.join(os.path.dirname(__file__), rpath)
tmpl = open(module_path('index.haml')).read().decode('utf-8')

def card2dict(card):
    output = {}
    lines = unfold(card)
    for line in lines:
        rowcol = line.split(':', 1)
        if len(rowcol) == 2:
            output[rowcol[0]] = rowcol[1]
    return output

@get('/')
def index():
    items = storage.ical.Collection.from_path('/test/carddav')
    return haml_template(tmpl, entries=items[1:], parse=card2dict)

@get('/static/<path:path>')
def serve_static(path):
    return static_file(path, root=module_path('static'))

def start_web_server():
    storage.load()

    run(host='localhost', port=8080)

if __name__ == '__main__':
    start_web_server()
