# Very simple tracing

import signal
import sys

tracefile = None


def tracer(frame, event, arg):
    # This can be interrupted by a signal....
    if tracefile:
        try:
            tracefile.write("%s %s: %s\n" % (event, frame.f_code.co_filename, frame.f_lineno))
            return tracer
        except exceptions.ValueError:
            # File was closed.
            pass
    return None


def trace_on(signum, frame):
    global tracefile
    if tracefile is None:
        tracefile = open('trace.txt', 'w')
        sys.settrace(tracer)
        

def trace_off(signum, frame):
    global tracefile
    existingfile = tracefile
    tracefile = None

    if existingfile:
        existingfile.close()

    sys.settrace(None)


def install_trace_handler():
    signal.signal(signal.SIGUSR1, trace_on)
    signal.signal(signal.SIGUSR2, trace_off)
