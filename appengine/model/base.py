from exc import NotFoundException, InvalidArgumentsException
from google.appengine.api import memcache
from google.appengine.ext import db
import logging

class BaseModel(db.Model):
    @classmethod
    def cache(cls, key=None, key_name=None):
        if key:
            obj = memcache.get(key)
            if not obj:
                logging.debug("(%s.cache) miss for %s" % (cls.__name__, key))
                obj = cls.get(key)
                memcache.set(key, obj, 60)
            else:
                logging.debug("(%s.cache) hit for %s" % (cls.__name__, key))

            return obj
        if key_name:
            key = cls.__name__ + "_" + key_name
            obj = memcache.get(key)
            if not obj:
                logging.debug("(%s.cache) miss for %s" % (cls.__name__, key))
                obj = cls.get_by_key_name(key_name)
                memcache.set(key, obj, 60)
            else:
                logging.debug("(%s.cache) hit for %s" % (cls.__name__, key))

            return obj

    def getKeyName(self):
        return self.key().name()

    @classmethod
    def update(cls, key=None, key_name=None, **kwargs):
        if key and key_name:
            raise InvalidArgumentsException("Must specify key OR key_name, not both.")
        if key:
            obj = cls.get(key)
        if key_name:
            obj = cls.get_by_key_name(key_name)
        if obj is None:
            raise NotFoundException()

        for k, v in kwargs.iteritems():
            obj.__setattr__(k, v)

        r = db.run_in_transaction(obj.put)
        logging.debug("%s.update: r = %s" % (obj.__class__.__name__, r))
        return r

class Constants(BaseModel):
    value = db.StringListProperty()
