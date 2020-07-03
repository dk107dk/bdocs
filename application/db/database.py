from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.app_config import AppConfig

class Database(object):
    """
        use to get an sql alchemy engine and session.
        use with closing. import closing from contextlib.
        this:
            engine = Database().engine
            with closing(Database.session(engine)()) as session:
        is exactly the same as:
            engine = Database().engine
            with closing(engine.session()) as session:
    """
    _url = None

    @classmethod
    def url(cls):
        if cls._url is None:
            cfg = AppConfig()
            user = cfg.get_with_default("db","user","root")
            password = cfg.get_with_default("db","password", "")
            host = cfg.get_with_default("db","host", "localhost")
            database = cfg.get_with_default("db","database", "seedocs")
            cls._url = f'mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}'
        return cls._url

    @classmethod
    def session(cls, engine):
        Session = sessionmaker(bind=engine)
        return Session

    @property
    def engine(self):
        url = Database.url()
        engine = create_engine(url, pool_size=5, echo=True)
        setattr(engine, "session", sessionmaker(bind=engine))
        return engine


