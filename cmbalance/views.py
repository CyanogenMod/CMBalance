from cmbalance.database.schema import File
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.response import Response
from pyramid.view import view_config
import os.path

@view_config(name='get')
def download(request):
    # Determine filename from request path.
    fn = os.path.split(request.path)[-1]
    file_obj = File.get_by_filename(fn)

    # 404 if the file does not exist.
    if file_obj == None:
        return HTTPNotFound()

    # otherwise, redirect to the full path
    url = "http://mirror.kanged.net/%s" % file_obj.full_path
    return HTTPFound(location=url)

    return Response("download")
