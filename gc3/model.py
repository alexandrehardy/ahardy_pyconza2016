import random

from twisted.internet import defer, reactor


class DBModel(object):
    database = 'db'
    table = 'table'

    def __init__(self):
        pass

    @classmethod
    def get(cls, identifier):
        result = cls()
        deferred = defer.Deferred()
        fields = cls.get_fields()

        for field in fields:
            if fields[field]:
                setattr(result, field, random.choice(fields[field]))

        result.id = identifier
        reactor.callLater(0, deferred.callback, result)
        return deferred

    def to_primitive(self):
        fields = self.get_fields()
        primitive = {}
        for field in fields:
            primitive[field] = getattr(self, field)
        return primitive


class Attendee(DBModel):
    database = 'pyconza2016'
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
