from unittest import TestCase
from remove_read_depth_only import PassFilter, FailFilter, DeletionFilter, EntryFilter

class TestPassFilter(TestCase):
    def test_call(self):
        pf = PassFilter()
        self.assertTrue(pf('IRRELEVANT'))

class TestFailFilter(TestCase):
    def test_call(self):
        ff = FailFilter()
        self.assertFalse(ff('ALSO_IRRELEVANT'))

class TestDeletionFilter(TestCase):
    def test_init(self):
        f = DeletionFilter()
        self.assertIsNotNone(f)

    def test_should_include(self):
        f = DeletionFilter()

        self.assertTrue(f.should_include('SI_BD_GARBAGE'))
        self.assertFalse(f.should_include('SOME_RANDOM_THING'))

    def test_should_exclude(self):
        f = DeletionFilter()

        self.assertTrue(f.should_exclude('YL_CN_CNVNATOR'))
        self.assertFalse(f.should_exclude('SOME_OTHER_RANDOM_THING'))

    def test_call(self):
        f = DeletionFilter()

        self.assertTrue(f(['SI_BD_GARBAGE', 'YL_CN_CNVNATOR']))
        self.assertTrue(f(['YL_CN_CNVNATOR', 'SI_BD_GARBAGE', 'YL_CN_CNVNATOR2']))
        self.assertFalse(f(['YL_CN_CNVNATOR', 'YL_CN_CNVNATOR2', 'YL_CN_CNVNATOR3']))
        self.assertFalse(f(['YL_CN_CNVNATOR', 'BI_GS_CNV_2', 'YL_CN_CNVNATOR3']))
        self.assertRaises(RuntimeError, f, ['YL_CN_CNVNATOR', 'THROW_AN_EXCEPTION'])
        
        f.exclude_prefixes = ( 'BE' )
        f.include_prefixes = ( 'BEE' )
        self.assertRaises(RuntimeError, f, ['BEEN', 'BEAN'])

class TestEntryFilter(TestCase):
    def test_init(self):
        f = EntryFilter()
        self.assertIsNotNone(f.callset_filter_lut)

    def test_call(self):
        f = EntryFilter()
        self.assertTrue(f('DEL_union', 'SI_BD_GARBAGE', ['YL_CN_CNVNATOR']))
        self.assertTrue(f('DEL_union', 'YL_CN_CNVNATOR', ['SI_BD_GARBAGE', 'YL_CN_CNVNATOR2']))
        self.assertFalse(f('DEL_union', 'YL_CN_CNVNATOR', ['YL_CN_CNVNATOR2', 'YL_CN_CNVNATOR3']))
        self.assertTrue(f('DEL_pindel', 'FAKE', None))
        self.assertFalse(f('NUMT_umich', 'FAKE', None))
        self.assertRaises(KeyError, f, 'INVALID_CALLSET', 'FAKE', None)


