from bottle import get, post, run
from radicale import storage

@get('/')
def index():
    items = storage.ical.Collection.from_path('/test/carddav')
    return '<html><body><pre>'+items[0].text+'</pre></body></html>'


def start_web_server():
    storage.load()

    run(host='localhost', port=8080)
