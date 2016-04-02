from waitress import serve

def wsgi_app(environ,start_responce):
    start_responce('200 OK', [('Content-Type', 'text/html')])
    path = environ['PATH_INFO'] 
    path = path[1:] 
    if (path == ''): 
        path = 'index.html' 
    file = open(path, 'r') 
    return [file.read().encode()]

class Wsgi_middleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_responce):
        response = self.app(environ, start_responce)[0].decode()
        print(response)
        if (response.find('<body>') != -1):
            head,body = response.split('<body>')
            bodytext,end = body.split('</body>')
            bodytext = '<body>' + "<div class='top'>Middleware TOP</div>" + bodytext + "<div class='bottom'>Middleware BOTTOM</div>" + '</body>'
            return [head.encode() + bodytext.encode() + end.encode()]
        else:
            return ["<div class='top'>Middleware TOP</div>" + response.encode() + "<div class='bottom'>Middleware BOTTOM</div>"]

wsgi_app = Wsgi_middleware(wsgi_app)
serve(wsgi_app, host = '', port = 8000)
