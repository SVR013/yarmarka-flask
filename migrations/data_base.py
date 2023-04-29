from collections import namedtuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, create_engine


class DataBase:
    def __init__(self, Table):
        engine = create_engine('sqlite:////home//funeralclown/yarmarka/migrations/yarmarka.db')
        self.session = Session(bind=engine)
        self.Table = Table
        self.query = self.session.query(Table)
        self.connection = engine.connect()
        self.desc = desc

    def gettuple(self, objquery) -> list:
        if objquery:
            if not isinstance(objquery, list | tuple):
                objquery = [objquery]
            list_tuples = []
            names = [name for name in objquery[0].__dict__.keys() if name[0] != '_']
            for q in objquery:
                Rez = namedtuple(f'{self.Table.__name__}', names)
                list_tuples.append(Rez(*[value for key, value in q.__dict__.items() if key in names]))
            return list_tuples[0] if len(list_tuples) == 1 else list_tuples

    def filter_request(self, **kwargs):
        names = set([name for name in self.Table.__dict__.keys() if name[0] != '_'])
        return dict([(key, value) for key, value in kwargs.items() if key in names])
