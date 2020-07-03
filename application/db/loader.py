import logging
from application.db.database import Database

class Loaded(object):

    def __init__(self):
        self._session = None
        self._engine = None
        self._thing = None

    def done(self):
        try:
            self.session.commit()
            self.session.close()
            self.engine.dispose()
        except:
            logging.error("Loaded.done: cannot close and dispose")

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    @property
    def thing(self):
        return self._thing

    @thing.setter
    def thing(self, value):
        self._thing = value


class Loader(object):
    """
        loads an entity by ID: User, Project, Team, Role. returns
        the entity in a Loaded, along with the session and engine
        used to find it. you must close the session and dispose the
        engine when you are done with the entity.
    """
    @classmethod
    def load(self, entity_class, theid) -> Loaded:
        loaded = Loaded()
        engine = Database().engine
        session = engine.session()
        thing = session.query(entity_class).filter_by(id=theid).first()
        session.commit()
        loaded.session = session
        loaded.engine = engine
        loaded.thing = thing
        return loaded

    @classmethod
    def load_by_name(self, entity_class, thename:str) -> Loaded:
        loaded = Loaded()
        engine = Database().engine
        session = engine.session()
        thing = session.query(entity_class).filter_by(name=thename).first()
        session.commit()
        loaded.session = session
        loaded.engine = engine
        loaded.thing = thing
        return loaded

