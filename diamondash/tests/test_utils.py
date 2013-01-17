from twisted.trial import unittest

from diamondash import utils


class UtilsTestCase(unittest.TestCase):
    def test_isint(self):
        """
        Should check if a number is equivalent to an integer
        """
        self.assertTrue(utils.isint(1))
        self.assertTrue(utils.isint(2.000))
        self.assertTrue(utils.isint(82734.0000000))
        self.assertTrue(utils.isint(-213.0))
        self.assertFalse(utils.isint(23123.123123))

    def test_format_value(self):
        def assert_format(input, expected):
            result = utils.format_value(input)
            self.assertEqual(result, expected)

        assert_format(999999, '999.999K')
        assert_format(1999999, '2.000M')
        assert_format(1234123456789, '1.234T')
        assert_format(123456123456789, '123.456T')
        assert_format(3.034992, '3.035')
        assert_format(2, '2')
        assert_format(2.0, '2')

    def test_format_time(self):
        def assert_format(input, expected):
            result = utils.format_time(input)
            self.assertEqual(result, expected)

        assert_format(1341318035, '2012-07-03 12:20')
        assert_format(1841318020, '2028-05-07 13:13')

    def test_slugify(self):
        """Should change 'SomethIng_lIke tHis' to 'something-like-this'"""
        self.assertEqual(utils.slugify('SoMeThing_liKe!tHis'),
                         'something-like-this')
        self.assertEqual(utils.slugify('Godspeed You! Black Emperor'),
                         'godspeed-you-black-emperor')

    def test_parse_interval(self):
        """
        Multiplier-suffixed intervals should be turned into integers correctly.
        """
        self.assertEqual(2, utils.parse_interval(2))
        self.assertEqual(2, utils.parse_interval("2"))
        self.assertEqual(2, utils.parse_interval("2s"))
        self.assertEqual(120, utils.parse_interval("2m"))
        self.assertEqual(7200, utils.parse_interval("2h"))
        self.assertEqual(86400 * 2, utils.parse_interval("2d"))

    def test_insert_defaults_by_key(self):
        """
        Should return a dict with the appropriate key's defaults, overidden
        with the original dict.
        """
        config = {'some_config_option': 23}
        defaults = {
            __name__: {
                'some_config_option': 42,
                'some_other_config_option': 182,
            },
            'some_other_module': {
                'some_config_option': 22,
                'another_config_option': 21,
            },
        }

        new_config = utils.insert_defaults_by_key(__name__, config, defaults)

        self.assertEqual(new_config, {
            'some_config_option': 23,
            'some_other_config_option': 182,
        })

        self.assertEqual(config, {'some_config_option': 23})

        self.assertEqual(defaults, {
            __name__: {
                'some_config_option': 42,
                'some_other_config_option': 182,
            },
            'some_other_module': {
                'some_config_option': 22,
                'another_config_option': 21,
            },
        })