import random

from twisted.internet import defer, reactor


class DBModel(object):
    database = 'db'
    table = 'table'
    _field_cache = {}

    def __init__(self):
        pass

    @staticmethod
    def get_fields(cls):
        if cls not in DBModel._field_cache:
            DBModel._field_cache[cls] = cls.get_fields()
        return DBModel._field_cache[cls]

    @classmethod
    def get(cls, identifier):
        result = cls()
        deferred = defer.Deferred()
        fields = DBModel.get_fields(cls)

        for field in fields:
            if fields[field]:
                setattr(result, field, random.choice(fields[field]))

        result.id = identifier
        reactor.callLater(0, deferred.callback, result)
        return deferred

    def to_primitive(self):
        fields = DBModel.get_fields(self.__class__)
        primitive = {}
        for field in fields:
            primitive[field] = getattr(self, field)
        return primitive


class Attendee(DBModel):
    database = 'pyconza'
    table = 'attendees'
    fields = {
            'id': [],
            'firstname': ['Joe', 'Mary', 'Tom', 'Bob',
                          'Alice', 'Ben', 'Ken', 'Rob',
                          'Sarah', 'Faith'],
            'surname': ['Brown', 'Smith', 'Green',
                        'Temple', 'Meyer', 'Basson',
                        'van der Merwe'],
            'interest': ['gc', 'cpu', 'python', 'django',
                         'twisted', 'memory', 'performance',
                         'debugging'],
    }

    @classmethod
    def get_fields(cls):
        return Attendee.fields
