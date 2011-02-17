from cmbalance.database.schema import Device, File
from cmbalance.resources import DownloadContext
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
import os.path
import urlparse

@view_config(renderer='browse.mako')
def browse(request):
    files = File.browse(request.params.get('device'),
                        request.params.get('type'))
    return {'request_type': request.params.get('type', None),
            'request_device': request.params.get('device', None),
            'devices': Device.get_all(), 'files': files}

@view_config(context=DownloadContext, renderer='interstitial.mako')
def download(context, request):
    VALID_REFERERS = ["mirror.cyanogenmod.com",
                      "mirror.teamdouche.net",
                      "download.cyanogenmod.com",
                      "localhost:6543"]
    referer = urlparse.urlparse(request.headers['Referer'])
    if referer.netloc not in VALID_REFERERS:
        return {'request_path': request.path, 'request_filename': os.path.basename(request.path)}
    else:
        try:
            url = "http://mirror.kanged.net/%s" % context.file_obj.full_path
            return HTTPFound(location=url)
        except:
            return HTTPNotFound()
