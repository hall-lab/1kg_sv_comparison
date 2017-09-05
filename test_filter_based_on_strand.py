import operator
from unittest import TestCase
from filter_based_on_strand import StrandFilter, OneThousandGenomesIntersect

class TestStrandFilter(TestCase):
    def test_init(self):
        obj = StrandFilter([(1, 1), (1, 1)])
        self.assertEqual(obj.allowable_strands, set([(1, 1)]))

    def test_call(self):
        obj1 = StrandFilter([('+', '-')])
        self.assertTrue(obj1('+', '-'))
        self.assertFalse(obj1('-', '+'))
        self.assertFalse(obj1(None, None))

    def test_multiple(self):
        obj1 = StrandFilter([('+', '-'), ('+', '+')])
        self.assertTrue(obj1('+', '-'))
        self.assertTrue(obj1('+', '+'))
        self.assertFalse(obj1('-', '+'))


class TestOneThousandGenomesIntersect(TestCase):
    def test_init(self):
        obj = OneThousandGenomesIntersect()
        self.assertTrue(obj.filters['DEL'])
        self.assertRaises(KeyError, operator.getitem, obj.filters, 'LOL')

    def test_call(self):
        obj = OneThousandGenomesIntersect()
        self.assertRaises(ValueError, obj, 'LOL', '-', '+')
        self.assertTrue(obj('DEL', '+', '-'))
        self.assertTrue(obj('INV', '-', '-'))
        self.assertFalse(obj('DEL', '+', '+'))

