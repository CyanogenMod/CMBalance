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
    file.filename = "update-cm-7.0.0-RC1-DesireHD-signed.zip"
    file.full_path = "RC/update-cm-7.0.0-RC1-DesireHD-signed.zip"
    file.type = 'RC'
    file.md5sum = "edad5b7c95b241dad1cd8623d29a00d5"
    file.device_id = 1
    file.size = 1204 ** 3
    session.add(file)

    # Make another file.
    file = File()
    file.filename = "update-cm-7.0.0-RC1-buzz-signed.zip"
    file.full_path = "RC/update-cm-7.0.0-RC1-buzz-signed.zip"
    file.type = 'RC'
    file.md5sum = '86c9c7047295c967cb954754a4c4dfd0'
    file.device_id = 2
    file.size = 1024 ** 2
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
