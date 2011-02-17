from cmbalance.database.schema import Device, File
from cmbalance.resources import DownloadContext
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config

@view_config(renderer='browse.mako')
def browse(request):
    files = File.browse(request.params.get('device'),
                        request.params.get('type'))
    return {'request_type': request.params.get('type', None),
            'request_device': request.params.get('device', None),
            'devices': Device.get_all(), 'files': files}

@view_config(context=DownloadContext)
def download(context, request):
    try:
        url = "http://mirror.kanged.net/%s" % context.file_obj.full_path
        return HTTPFound(location=url)
    except:
        return HTTPNotFound()
