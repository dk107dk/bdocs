import logging
from application.db.database import Database
from application.db.entities import Base, RoleEntity, Roles, SubscriptionEntity
from application.users.user import User
from contextlib import closing
from enum import Enum


class Standup(object):

    def __call__(self):
        print(f"Standup.__call__: standing up database")
        engine = Database().engine
        with closing(engine.session()) as session:
            print(f"Standup.__call__: creating all tables using {engine}, {session}")
            Base.metadata.create_all(engine)
            roles = [RoleEntity(id=Roles.OWNER.value, name=Roles.OWNER.value),\
                     RoleEntity(id=Roles.MEMBER.value, name=Roles.MEMBER.value),\
                     RoleEntity(id=Roles.VIEWER.value, name=Roles.VIEWER.value)]
            print(f"Standup.__call__: creating roles: {roles}")
            session.add_all(roles)
            session.commit()
            subscription = SubscriptionEntity(\
                name='Free tier',users=2,roots=1,projects=1,teams=1,team_members=0,\
                docs=200,each_doc_bytes=1000000,total_doc_bytes=50000000,api_keys=1,\
                api_calls=0,api_cycle='Monthly',subscription_cycle='Monthly')
            print(f"Standup.__call__: creating subscription: {subscription}")
            session.add(subscription)
            session.commit()
            admin = User(system_admin=True, given_name='Sam', family_name='Bats', user_name='admin')
            print(f'Standup.__call__: creating admin user: {admin}')
            admin.create_me(session, subscriptionid=subscription.id)
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


