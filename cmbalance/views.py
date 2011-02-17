from cmbalance.database.schema import Device
from cmbalance.resources import DownloadContext
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

@view_config(renderer='browse.mako')
def browse(request):
    return {'devices': Device.get_all()}

@view_config(context=DownloadContext)
def download(context, request):
    url = "http://mirror.kanged.net/%s" % context.file_obj.full_path
    print "Redirecting to '%s'" % url
    return HTTPFound(location=url)
