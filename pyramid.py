from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

def aboutme(request):
	file = open('about/aboutme.html', 'r')
	data = file.read()
	file.close()
	return Response(data)

def index(request):
	file = open('index.html', 'r')
	data = file.read()
	file.close()
	return Response(data)

class middleWare(object):
	def __init__(self, app):
		self.app = app
	def __call__(self, environ, start_response):
		html = self.app(environ, start_response)[0].decode()
		top = '<div class=''top''>Middleware TOP</div>'
		bottom = '<div class=''bottom''>Middleware BOTTOM</div>'
		head, body = html.split('<body>')
		data, end = body.split('</body>')
		data = '<body>' + top + data + bottom + '</body>'
		return [head.encode('utf8') + data.encode('utf8') + end.encode('utf8')]		


if __name__ == '__main__':
	config = Configurator()
	config.add_route('default', '/')
	config.add_view(index, route_name = 'default')
	config.add_route('index', '/index.html')
	config.add_view(index, route_name = 'index')
	config.add_route('aboutme', '/about/aboutme.html')
	config.add_view(aboutme, route_name = 'aboutme')
	wsgi_app = middleWare(config.make_wsgi_app())
	server = make_server('0.0.0.0', 8000, wsgi_app)
	server.serve_forever()
