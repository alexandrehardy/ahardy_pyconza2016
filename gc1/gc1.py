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

    @defer.inlineCallbacks
    def get_attendees(self):
        attendees = [(yield self.get_attendee_from_db(registration)) for registration in xrange(0, 1000)]
        defer.returnValue(attendees)

    @defer.inlineCallbacks
    def render_list(self, request):
        db_results = yield self.get_attendees()
        self.log('Got results %s' % len(db_results))
        results = [r.to_primitive() for r in db_results]
        self.log('Shipped results %s' % len(results))
        request.write(json.dumps(results, indent=4))
        request.finish()
        self.log('All done')

    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        self.render_list(request)
        return server.NOT_DONE_YET


if __name__ == '__main__':
    site = server.Site(Demo())
    reactor.listenTCP(8080, site)
    manhole = ShellFactory()
    manhole.username = 'demo'
    manhole.password = 'demo'
    reactor.listenTCP(20000, manhole)
    print 'Running web server, pid=%s' % os.getpid()
    open('gc.pid', 'w').write('%s' % os.getpid())
    reactor.run()
    print 'Stopped!'
