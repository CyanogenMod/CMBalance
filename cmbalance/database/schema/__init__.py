from cmbalance import cache
from cmbalance.database import Base, DBSession
from cmbalance.lib.string import convert_bytes
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.util import join
from sqlalchemy.sql.expression import func, desc

class File(Base):
    __tablename__ = "files"

    id = Column('id', Integer, primary_key=True)
    filename = Column('filename', String(255), unique=True)
    size = Column('size', Integer)
    full_path = Column('full_path', String(255))
    md5sum = Column('md5sum', String(32))

    device_id = Column('device_id', Integer, ForeignKey('devices.id'), nullable=False)
    device = relation('Device')
    type = Column('type', String(20), index=True)

    date_created = Column(DateTime, default=func.now())
    date_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    @property
    def human_size(self):
        return convert_bytes(self.size)

    @classmethod
    def get_by_filename(cls, filename):
        def get_from_database():
            session = DBSession()
            try:
                file = session.query(cls).filter(cls.filename == filename).one()
            except NoResultFound:
                file = None

            session.close()
            DBSession.remove()

            return file

        file_cache = cache.get_cache('file', expire=60)
        file = file_cache.get(filename, createfunc=get_from_database)
        return file

    @classmethod
    def browse(cls, device, type):
        cache_key = "%s_%s" % (device or "null", type or "null")
        browse_cache = cache.get_cache('browse', expire=60)

        def get_from_database():
            session = DBSession()
            query = session.query(cls)

            if device is not None:
                query = query.select_from(join(File, Device)). \
                            filter(Device.name == device)

            if type is not None:
                query = query.filter(cls.type == type)

            # Limit the query and order it
            query = query.order_by(desc(cls.date_created))[:20]

            session.close()
            DBSession.remove()

            return query

        return browse_cache.get(cache_key, createfunc=get_from_database)

class Device(Base):
    __tablename__ = "devices"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50), unique=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, name):
        session = DBSession()

        try:
            device = session.query(cls).filter(cls.name == name).one()
        except:
            device = None

        session.close()
        DBSession.remove()

        return device

    @classmethod
    def get_all(cls):
        def get_from_database():
            session = DBSession()
            try:
                devices = session.query(cls).order_by(cls.name).all()
            except:
                devices = None

            session.close()
            DBSession.remove()

            return devices

        devices_cache = cache.get_cache('all', expire=3600)
        return devices_cache.get('all', createfunc=get_from_database)
