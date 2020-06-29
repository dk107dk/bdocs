from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.app_config import AppConfig

class SessionFactory(object):
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

    def __init__(self):
        self._session = None
        self._engine = None

    def _init(self):
        url = SessionFactory.url()
        engine = create_engine(url, pool_size=5, echo=True)
        self._engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self._session = session

    @property
    def session(self):
        if self._session is None:
            self._init()
        return self._session

    @property
    def engine(self):
        if self._engine is None:
            self._init()
        return self._engine

