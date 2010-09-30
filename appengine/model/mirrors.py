from google.appengine.ext import db
from model.base import BaseModel

class Mirror(BaseModel):
    name = db.StringProperty()
    owner = db.StringProperty(required=True)
    link = db.LinkProperty()
    url = db.LinkProperty(required=True)
    ip = db.StringProperty()
    control_type = db.StringProperty(required=True)
    enabled = db.BooleanProperty(required=True, default=True)
    status = db.StringProperty()
    location = db.StringProperty()
    last_seen = db.DateTimeProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)

class MirrorHits(BaseModel):
    count = db.IntegerProperty(required=True, default=0)

    @classmethod
    def increment(cls, key):
        count = cls.get_by_key_name(key)
        if count is None:
            count = cls(key_name=key)

        count.count += 1
        count.put()
