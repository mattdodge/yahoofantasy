from collections import namedtuple
from unittest import TestCase
from yahoofantasy.stats.utils import get_stat_and_value


StatResult = namedtuple('StatObj', ['stat_id', 'value'])


class TestStatUtils(TestCase):

    def test_get_stat_and_value(self):
        # String stat ID and stat value
        self.assertEqual(
            get_stat_and_value(StatResult('60', '65/290')),
            ('H/AB', '65/290'),
        )
        # Integer stat ID and stat value
        self.assertEqual(
            get_stat_and_value(StatResult(7, 50)),
            ('R', 50),
        )
