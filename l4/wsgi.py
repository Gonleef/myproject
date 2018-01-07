from webob import Request
from jinja2 import Environment, FileSystemLoader

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
environment = Environment(loader = FileSystemLoader('.'))	    
class WsgiTopBottomMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):       
    
            css = []
            js = []
            for include in includes:
                if(include.split('.')[1] == 'css'):
                    css.append(include)
                else:
                    js.append(include)
	    
            response = self.app(environ, start_response).decode() 
            return (response).encode()  	    

def app(environ, start_response):
    addr = environ['PATH_INFO']
    path = '.' + addr  
    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])
    template = enviroment.get_template(path)
    return template.render(css= css, js= js).encode()

app = WsgiTopBottomMiddleware(app)

print(Request.blank('/index.html').get_response(app))
