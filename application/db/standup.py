import logging
from application.db.session_factory import SessionFactory
from application.db.entities import Base, Role

class Standup(object):

    def __call__(self):
        print(f"Standup.__call__: standing up database")
        sf = SessionFactory()
        session = sf.session
        engine = sf.engine
        print(f"Standup.__call__: creating all tables using {engine}, {session}")
        Base.metadata.create_all(engine)
        roles = [Role(name='Owner'),Role(name='Member'),Role(name='Viewer')]
        print(f"Standup.__call__: creating roles: {roles}")
        session.add_all(roles)
        session.commit()
        engine.dispose()
        print(f"Standup.__call__: stood up database")

class Shutdown(object):

    def __call__(self):
        print(f"Shutdown.__call__: shutting down database")
        sf = SessionFactory()
        session = sf.session
        engine = sf.engine
        print(f"Shutdown.__call__: dropping all tables using {engine}, {session}")
        Base.metadata.drop_all(engine)
        session.commit()
        engine.dispose()
        print(f"Shutdown.__call__: shut down database")


