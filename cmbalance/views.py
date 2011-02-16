from pyramid.response import Response
from pyramid.view import view_config

@view_config(name='get')
def download(request):
    return Response("download")
