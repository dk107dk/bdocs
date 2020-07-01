import logging
from application.db.database import Database
from application.db.entities import Base, RoleEntity
from contextlib import closing

class Standup(object):

    def __call__(self):
        print(f"Standup.__call__: standing up database")
        engine = Database().engine
        with closing(engine.session()) as session:
            print(f"Standup.__call__: creating all tables using {engine}, {session}")
            Base.metadata.create_all(engine)
            roles = [RoleEntity(name='Owner'),RoleEntity(name='Member'),RoleEntity(name='Viewer')]
            print(f"Standup.__call__: creating roles: {roles}")
            session.add_all(roles)
            session.commit()
        engine.dispose()
        print(f"Standup.__call__: stood up database")

class Shutdown(object):

    def __call__(self):
        print(f"Shutdown.__call__: shutting down database")
        engine = Database().engine
        #
        # this:
        #     with closing(Database.session(engine)()) as session:
        # is exactly the same as the below:
        #
        with closing(engine.session()) as session:
            print(f"Shutdown.__call__: dropping all tables using {engine}, {session}")
            Base.metadata.drop_all(engine)
            session.commit()
        engine.dispose()
        print(f"Shutdown.__call__: shut down database")


