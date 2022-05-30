from lesson_1.templates import render_


def index_view(request):
    print(request)
    return '200 OK', render_('index.html', color_name='none')


def black_view(request):
    print(request)
    return '200 OK', render_('index.html', color_name='black')


def red_view(request):
    print(request)
    return '200 OK', render_('index.html', color_name='red')


def white_view(request):
    print(request)
    return '200 OK', render_('index.html', color_name='white')


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 UNKNOWN COLOR!!!!!!1']


class Other:
    def __call__(self, request):
        return '200 OK', render_('index.html', color_name='other color')


routes = {
    '/': index_view,
    '/black/': black_view,
    '/red/': red_view,
    '/white/': white_view,
    '/other/': Other()
}


def opposite_color_front(request):
    request['opposite_color'] = 'opposite color'


def similar_color_front(request):
    request['similar_color'] = 'similar color'


fronts = [opposite_color_front, similar_color_front]


class Application:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):

        print('working...')
        path = environ['PATH_INFO']
        view = not_found_404_view
        if path in self.routes:
            view = self.routes[path]
        request = {}
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return body.encode('utf-8')


application = Application(routes, fronts)

