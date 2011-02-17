from cmbalance.database.base import AbstractTable
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base(cls=AbstractTable)

def populate_data():
    from cmbalance.database.schema import Device, File
    session = DBSession()

    # Create devices.
    for device in ["ace", "buzz", "bravo", "bravoc", "dream_sapphire", "espresso", "hero", "heroc", "inc", "liberty", "legend", "passion", "sholes", "supersonic", "one", "z71", "crespo", "glacier", "vision"]:
        device_obj = Device(name=device)
        session.add(device_obj)

    # Create a file entry.
    file = File()
    file.filename = "derp.zip"
    file.full_path = "derp.zip"
    file.md5sum = "xyz"
    file.device_id = 1
    session.add(file)

    session.commit()
    session.close()

def init_database(engine):
    DBSession.configure(bind=engine)

    # Import ORM mapped objects.
    __import__("cmbalance.database.schema", globals(), locals(), ["*"])

    # Bind metadata to engine.
    Base.metadata.bind = engine

    # Create all tables.
    Base.metadata.create_all(engine)

    # Create some test data.
    try:
        populate_data()
    except IntegrityError:
        DBSession.rollback()
