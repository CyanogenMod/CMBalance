from sqlalchemy.orm.session import Session

class AbstractTable(object):
    @property
    def session(self):
        return Session.object_session(self)
