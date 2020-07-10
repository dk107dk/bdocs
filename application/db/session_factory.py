from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.app_config import AppConfig

class SessionFactory(object):
    _url = None

    @classmethod
    def url(cls):
        if cls._url is None:
            cfg = AppConfig()
            user = cfg.get("db","user","root")
            password = cfg.get("db","password", "")
            host = cfg.get("db","host", "localhost")
            database = cfg.get("db","database", "seedocs")
            cls._url = f'mysql+mysqlconnector://{user}:{password}@{host}:3306/{database}'
        return cls._url

    @property
    def engine(self):
        url = SessionFactory.url()
        engine = create_engine(url, pool_size=5, echo=True)
        return engine

    @classmethod
    def session(cls, engine):
        Session = sessionmaker(bind=engine)
        return Session




