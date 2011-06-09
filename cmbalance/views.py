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
    # The following domains are allowed to directly link to us.
    VALID_REFERERS = ["mirror.cyanogenmod.com",
                      "mirror.teamdouche.net",
                      "download.cyanogenmod.com",
                      "localhost:6543"]

    # Pull referer from http headers.
    referer = request.headers.get('Referer', None)

    # Check that the referring domain is allowed.
    if referer and urlparse.urlparse(referer).netloc not in VALID_REFERERS:
        return {'request_path': request.path,
                'request_filename': os.path.basename(request.path)}
    elif getattr(context, 'file_obj', None):
        url = "http://mirrorbrain.cyanogenmod.com/cm/%s" % context.file_obj.full_path
        return HTTPFound(location=url)
    else:
        return HTTPNotFound()
