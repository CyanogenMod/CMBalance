from cmbalance.database.schema import File
import os.path

class DownloadContext(object):
    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        filename = os.path.split(self.request.path)[-1]
        file_obj = File.get_by_filename(filename)
        if file_obj is not None:
            self.file_obj = file_obj
            return self
        else:
            raise KeyError

class Root(object):
    def __init__(self, request):
        self.request = request
    def __getitem__(self, key):
        if key in ["get", "download"]:
            return DownloadContext(self.request)
        else:
            raise KeyError
