from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

DB_URL = "sqlite:///:memory:"

Base = declarative_base()

class Poem(Base):
    __tablename__ = 'poems'

    id = Column(Integer, primary_key=True)
    poem = Column(String)
    author = Column(String)
    _keywords = Column(String, default="")
    stars = Column(Integer, default=0)
    flags = Column(Integer, default=0)

    @property
    def keywords(self):
        return [x for x in self._keywords.split()]

    @keywords.setter
    def keywords(self, keyword):
        if self._keywords is None:
            self._keywords = keyword
        else:
            self._keywords += " {}".format(keyword)

    def __repr__(self):
       return "<Poem(id={}, poem={}, author={}, keywords={})>".format(self.id, \
                                        self.poem, self.author, self.keywords)

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            wrapper.return_value = f(*args, **kwargs)
        return wrapper.return_value
    wrapper.has_run = False
    wrapper.return_value = None
    return wrapper

@run_once
def get_db_engine():
    engine = create_engine(DB_URL, echo=True)
    Base.metadata.create_all(engine)
    return engine

def get_db_sess():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()