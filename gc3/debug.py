import gc
import sys


class MemDebug(object):
    exclude = [
                  "frame",
                  "cell",
                  "weakref",
              ]
    def __init__(self):
        self.set_base()

    def set_base(self):
        self.base_ids = []
        self.base_idmap = {}
        self.bytype = {}
        self.sizes = {}

        gc.collect()
        gc.collect()

        self.base_ids = [id(i) for i in gc.get_objects()]
        self.base_idmap = {}
        for i in self.base_ids:
            self.base_idmap[i] = 1
        del i

    def analyze(self):
        self.bytype = {}
        self.sizes = {}

        gc.collect()
        gc.collect()
        restricted = [id(self), id(self.base_ids), id(self.base_idmap), id(self.bytype), id(self.sizes)]
        restricted.append(id(restricted))

        leaked = [i for i in gc.get_objects() if id(i) not in restricted and id(i) not in self.base_idmap]

        for i in leaked:
            if id(i) == id(leaked):
                continue

            t = str(type(i))
            if t in self.bytype:
                self.bytype[t].append(i)
            else:
                self.bytype[t] = [i]

        del leaked

        for k, v in self.bytype.iteritems():
            self.sizes[k] = sum([sys.getsizeof(i) for i in v])

    def interested_in(self, obj):
        if getattr(obj, "__class__", None):
            if obj.__class__.__name__ not in self.exclude:
                return True
            else:
                return False
        return True

    def refs(self, obj):
        gc.collect()
        gc.collect()
        restricted = [id(self), id(self.base_ids), id(self.base_idmap), id(self.bytype), id(self.sizes)]
        for v in self.bytype.values():
            restricted.append(id(v))
        restricted.append(id(restricted))
        return [i for i in gc.get_referrers(obj) if id(i) not in restricted and self.interested_in(i)]

    def type(self, t):
        return self.bytype[t]

    def top(self, n):
        i = 0
        for k, v in sorted(self.sizes.items(), key=lambda r: r[1], reverse=True):
            print "    %s: %s" % (k, v)
            i = i + 1
            if i > n:
                return

    @staticmethod
    def dump_pointers():
        f = open('pointers.txt', 'w')
        for obj in gc.get_objects():
            f.write('%s,%s\n' % (id(obj), sys.getsizeof(obj)))
        f.close()
