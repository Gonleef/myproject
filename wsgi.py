from paste.httpserver import serve

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


class WsgiTopBottomMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response).decode()  # bytes to str
        css = "";
        js = "";
        for include in includes:
            if(include.split('.')[1] == 'css'):
                css += '<link rel="stylesheet" href="/_static/' + include + '"/>\n'
            elif(include.split('.')[1] == 'js'):
                js += '<script src="/_static/' + include + '"></script>\n'
        
        if response.find('<head>') > -1:
            data, htmlend = response.split('</head>')
            response = data + css + '</head>' + htmlend
        if response.find('<body>') > -1:
            header, body = response.split('<body>')
            data, htmlend = body.split('</body>')
            response = header + '<body>' + data + js + '</body>' + htmlend
            yield (response).encode()  # str to bytes
        else:
            yield ('').encode()  # str to bytes


def app(environ, start_response):
    
    path = environ['PATH_INFO']
    
    if path == '/index.html' or '/' or '/about/aboutme.html':    
        file = open('.' + path, 'r')
        page = file.read()
        file.close()
        response_code = '200 OK'
            
        response_type = ('Content-Type', 'text/HTML')
        start_response(response_code, [response_type])
        return page;
    else:
        response_code = '404 Not Found'
        response_type = ('Content-Type', 'text/HTML')
        start_response(response_code, [response_type])
        
        return "".encode()

# Оборачиваем WSGI приложение в middleware
app = WsgiTopBottomMiddleware(app)

# Запускаем сервер
serve(app, host='localhost', port=8000)
