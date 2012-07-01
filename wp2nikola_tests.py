from datetime import datetime
import unittest

from wp2nikola import WordpressImporter


class DateConversionTest(unittest.TestCase):
    def test_conversion(self):
        date_from_wordpress = 'Sun, 17 Jun 2012 19:20:59 +0000'

        # The format Nikola expects: '%Y/%m/%d %H:%M'
        self.assertEqual(datetime(2012, 06, 17, 19, 20), WordpressImporter.convert_date(date_from_wordpress))

if __name__ == '__main__':
    unittest.main()
