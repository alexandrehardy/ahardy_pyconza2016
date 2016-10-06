import json
import os
import time

from twisted.web import server, resource
from twisted.internet import defer, reactor
# Should use twisted.conch.manhole and twisted.conch.telnet
from twisted.manhole.telnet import ShellFactory

from model import Attendee


class Demo(resource.Resource):
    isLeaf = True
    _logs = []

    def log(self, message):
        self._logs.append('%s: %s' % (time.time(), message))
        # Only keep the last ten log lines
        self._logs = self._logs[-10:]

    def get_attendee_from_db(self, registration_number):
        class NewAttendee(Attendee):
            database = 'pyconza2016'
        return NewAttendee.get(registration_number)

    def get_db_cursor(self):
        # Pretend to be a cursor!
        for registration in xrange(0, 1000):
            yield self.get_attendee_from_db(registration)

    @defer.inlineCallbacks
    def get_attendees(self):
        # Pretend to contact the database, need this to be a generator
        yield True
        defer.returnValue(self.get_db_cursor())

    @defer.inlineCallbacks
    def render_list(self, request):
        db_results = yield self.get_attendees()
        self.log('Got results')
        request.write('[\n')

        # Get the first value. We should be checking for StopIteration here ...
        first = yield db_results.next()
        request.write(json.dumps(first.to_primitive(), indent=4))

        for deferred_result in db_results:
            result = yield deferred_result
            request.write(',\n%s' % json.dumps(result.to_primitive(), indent=4))

        request.write('\n]\n')
        self.log('Shipped results')
        request.finish()
        self.log('All done')

    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        self.render_list(request)
        return server.NOT_DONE_YET


@defer.inlineCallbacks
def audit():
    work = []
    i = 0
    while True:
        i = i + 1
        work.append('work %s' % i)
        deferred = defer.Deferred()
        reactor.callLater(0.0001, deferred.callback, True)
        yield deferred

        if len(work) > 10000:
            # remove every second item
            work = work[::2]


if __name__ == '__main__':
    site = server.Site(Demo())
    reactor.listenTCP(8080, site)
    manhole = ShellFactory()
    manhole.username = 'demo'
    manhole.password = 'demo'
    reactor.listenTCP(20000, manhole)
    reactor.callLater(0, audit)
    print 'Running web server, pid=%s' % os.getpid()
    open('gc.pid', 'w').write('%s' % os.getpid())
    reactor.run()
    print 'Stopped!'
