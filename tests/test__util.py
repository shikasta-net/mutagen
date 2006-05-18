from mutagen._util import DictMixin, cdata
from tests import TestCase, add

class FDict(DictMixin):
    def __init__(self):
        self.__d = {}
        self.keys = self.__d.keys

    def __getitem__(self, *args): return self.__d.__getitem__(*args)
    def __setitem__(self, *args): return self.__d.__setitem__(*args)
    def __delitem__(self, *args): return self.__d.__delitem__(*args)

class TDictMixin(TestCase):
    def setUp(self):
        self.fdict = FDict()
        self.rdict = {}
        self.fdict["foo"] = self.rdict["foo"] = "bar"

    def test_getsetitem(self):
        self.failUnlessEqual(self.fdict["foo"], "bar")
        self.failUnlessRaises(KeyError, self.fdict.__getitem__, "bar")

    def test_has_key_contains(self):
        self.failUnless("foo" in self.fdict)
        self.failIf("bar" in self.fdict)
        self.failUnless(self.fdict.has_key("foo"))
        self.failIf(self.fdict.has_key("bar"))

    def test_keys(self):
        self.failUnlessEqual(list(self.fdict.keys()), list(self.rdict.keys()))
        self.failUnlessEqual(
            list(self.fdict.iterkeys()), list(self.rdict.iterkeys()))

    def test_values(self):
        self.failUnlessEqual(
            list(self.fdict.values()), list(self.rdict.values()))
        self.failUnlessEqual(
            list(self.fdict.itervalues()), list(self.rdict.itervalues()))

    def test_items(self):
        self.failUnlessEqual(list(self.fdict.items()), list(self.rdict.items()))
        self.failUnlessEqual(
            list(self.fdict.iteritems()), list(self.rdict.iteritems()))

    def test_pop(self):
        self.failUnlessEqual(self.fdict.pop("foo"), self.rdict.pop("foo"))
        self.failUnlessRaises(KeyError, self.fdict.pop, "woo")

    def test_popitem(self):
        self.failUnlessEqual(self.fdict.popitem(), self.rdict.popitem())
        self.failUnlessRaises(KeyError, self.fdict.popitem)

    def test_update_other(self):
        other = {"a": 1, "b": 2}
        self.rdict.update(other)
        self.fdict.update(other)

    def test_setdefault(self):
        self.fdict.setdefault("foo", "baz")
        self.rdict.setdefault("foo", "baz")
        self.fdict.setdefault("bar", "baz")
        self.rdict.setdefault("bar", "baz")

    def test_get(self):
        self.failUnlessEqual(self.rdict.get("a"), self.fdict.get("a"))
        self.failUnlessEqual(self.rdict.get("a", "b"), self.fdict.get("a", "b"))
        self.failUnlessEqual(self.rdict.get("foo"), self.fdict.get("foo"))

    def test_repr(self):
        self.failUnlessEqual(repr(self.rdict), repr(self.fdict))

    def test_len(self):
        self.failUnlessEqual(len(self.rdict), len(self.fdict))

    def tearDown(self):
        self.failUnlessEqual(self.fdict, self.rdict)
        self.failUnlessEqual(self.rdict, self.fdict)

add(TDictMixin)

class Tcdata(TestCase):
    ZERO = "\x00\x00\x00\x00"
    LEONE = "\x01\x00\x00\x00"
    BEONE = "\x00\x00\x00\x01"
    NEGONE = "\xff\xff\xff\xff"

    def test_int_le(self):
        self.failUnlessEqual(cdata.int_le(self.ZERO), 0)
        self.failUnlessEqual(cdata.int_le(self.LEONE), 1)
        self.failUnlessEqual(cdata.int_le(self.BEONE), 16777216)
        self.failUnlessEqual(cdata.int_le(self.NEGONE), -1)

    def test_uint_le(self):
        self.failUnlessEqual(cdata.uint_le(self.ZERO), 0)
        self.failUnlessEqual(cdata.uint_le(self.LEONE), 1)
        self.failUnlessEqual(cdata.uint_le(self.BEONE), 16777216)
        self.failUnlessEqual(cdata.uint_le(self.NEGONE), 2**32-1)

    def test_longlong_le(self):
        self.failUnlessEqual(cdata.longlong_le(self.ZERO * 2), 0)
        self.failUnlessEqual(cdata.longlong_le(self.LEONE + self.ZERO), 1)
        self.failUnlessEqual(cdata.longlong_le(self.NEGONE * 2), -1)

    def test_ulonglong_le(self):
        self.failUnlessEqual(cdata.ulonglong_le(self.ZERO * 2), 0)
        self.failUnlessEqual(cdata.ulonglong_le(self.LEONE + self.ZERO), 1)
        self.failUnlessEqual(cdata.ulonglong_le(self.NEGONE * 2), 2**64-1)

    def test_invalid_lengths(self):
        self.failUnlessRaises(cdata.error, cdata.int_le, "")
        self.failUnlessRaises(cdata.error, cdata.longlong_le, "")
        self.failUnlessRaises(cdata.error, cdata.uint_le, "")
        self.failUnlessRaises(cdata.error, cdata.ulonglong_le, "")

    def test_test(self):
        self.failUnless(cdata.test_bit((1), 0))
        self.failIf(cdata.test_bit(1, 1))

        self.failUnless(cdata.test_bit(2, 1))
        self.failIf(cdata.test_bit(2, 0))

        v = (1 << 12) + (1 << 5) + 1
        self.failUnless(cdata.test_bit(v, 0))
        self.failUnless(cdata.test_bit(v, 5))
        self.failUnless(cdata.test_bit(v, 12))
        self.failIf(cdata.test_bit(v, 3))
        self.failIf(cdata.test_bit(v, 8))
        self.failIf(cdata.test_bit(v, 13))

add(Tcdata)