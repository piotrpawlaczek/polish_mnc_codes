import unittest
import warnings
import collections


class WarningTestMixin(object):
    'A test which checks if the specified warning was raised'

    def assertWarns(self, warning, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')
            result = callable(*args, **kwds)
            self.assertTrue(any(item.category == warning for item in warning_list))

class TestMNCCodesCorrect(WarningTestMixin, unittest.TestCase):

    def setUp(self):
        from mnc_grabber import MNCCodes
        from mnc_grabber import UKE_URL, FILENAME
        self.codes = MNCCodes()

    def test_type(self):
        # check if instance is of hashable type
        self.assertIsInstance(self.codes, collections.Mapping)

    def test_warnings(self):
        from mnc_grabber import MNCCodes
        self.assertWarns(UserWarning,
                         MNCCodes,
                         filename='filename_has_changed')

    def test_invalid_source(self):
        from mnc_grabber import MNCCodes
        self.assertRaises(ValueError, MNCCodes, source='invalid')

    def test_capicity(self):
        self.assertGreater(len(self.codes), 0)

    def test_behaviour(self):
        self.codes['test'] = 'test'
        self.assertEqual(self.codes['test'], 'test')
        self.assertIsNotNone(self.codes.pop('test'))



if __name__ == '__main__':
    from mnc_grabber import MNCCodes
    codes = MNCCodes()
    for item in codes.iteritems():
        print ' - '.join(item)
    unittest.main()
