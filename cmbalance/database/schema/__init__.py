from cmbalance.database import Base, DBSession
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relation
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

class Device(Base):
    __tablename__ = "devices"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50), index=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def get_by_name(cls, name):
        session = DBSession()

        try:
            device = session.query(cls).filter(cls.name == name).one()
        except:
            device = None

        return device
