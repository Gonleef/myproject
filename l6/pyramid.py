
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from jinja2 import FileSystemLoader,Environment
import os
from pyramid.response import Response

includes = [
                'app.js',
                'react.js',
                'leaflet.js',
                'D3.js',
                'moment.js',
                'math.js',
                'main.css',
                'bootstrap.css',
                'normalize.css',
            ]

css = []
js = []
for include in includes:
    if(include.split('.')[1] == 'css'):
        css.append(include)
    else:
        js.append(include)
	        

def index(request):
    env = Environment(loader=FileSystemLoader('.'))  
    res = env.get_template('/index.html').render({'css': css, 'js': js}) 
    return Response(res)

def aboutme(request):
    env = Environment(loader=FileSystemLoader('.'))
    res = env.get_template('aboutme/aboutme.html').render({'css': css, 'js': js})
    return Response(res)

if __name__ == '__main__':
    configurator = Configurator()
    configurator.add_route('aboutme', '/aboutme/aboutme.html')
    configurator.add_view(aboutme, route_name='aboutme')
    configurator.add_route('index', '/index.html')
    configurator.add_view(index, route_name='index')
    app = configurator.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
	server.serve_forever()
