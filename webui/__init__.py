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

def parse_raw(cards):
    output = []
    card   = None
    lines = cards.split('\n')
    for line in lines:
        if line.strip().upper() == u'BEGIN:VCARD':
            card = [line]
        elif line.strip().upper() == u'END:VCARD':
            card += [line]
            output.append(u'\n'.join(card))
            card = None
        elif card != None:
            card += [line]
        else:
            pass
    return map(card2dict, output)


@get('/')
def index():
    items = storage.ical.Collection.from_path('/nilksa/AddressBook')
    return haml_template(tmpl, entries=parse_raw(items[1].text))

@get('/static/<path:path>')
def serve_static(path):
    return static_file(path, root=module_path('static'))

def start_web_server():
    storage.load()

    run(host='localhost', port=8080)

if __name__ == '__main__':
    start_web_server()
