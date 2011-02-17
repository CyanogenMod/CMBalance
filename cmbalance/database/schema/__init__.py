from cmbalance import cache
from cmbalance.database import Base, DBSession
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import func

class File(Base):
    __tablename__ = "files"

    id = Column('id', Integer, primary_key=True)
    filename = Column('filename', String(255), index=True)
    full_path = Column('full_path', String(255))
    md5sum = Column('md5sum', String(32))

    device_id = Column('device_id', Integer, ForeignKey('devices.id'), nullable=False)
    device = relation('Device')

    date_created = Column(DateTime, default=func.now())
    date_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    @classmethod
    def get_by_filename(cls, filename):
        def get_from_database():
            session = DBSession()
            try:
                file = session.query(cls).filter(cls.filename == filename).one()
            except NoResultFound:
                file = None

            return file

        file_cache = cache.get_cache('file', expire=60)
        file = file_cache.get(filename, createfunc=get_from_database)
        return file

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

        return device

    @classmethod
    def get_all(cls):
        def get_from_database():
            session = DBSession()
            try:
                devices = session.query(cls).order_by(cls.name).all()
            except:
                devices = None

            return devices

        devices_cache = cache.get_cache('all', expire=3600)
        return devices_cache.get('all', createfunc=get_from_database)
