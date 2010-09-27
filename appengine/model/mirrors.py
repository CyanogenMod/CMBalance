from google.appengine.ext import db
from model.base import BaseModel

class Mirror(BaseModel):
    owner = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    ip = db.StringProperty()
    control_type = db.StringProperty(required=True)
    enabled = db.BooleanProperty(required=True, default=True)
    last_seen = db.DateTimeProperty(auto_now=True)
    date_added = db.DateTimeProperty(auto_now_add=True)
