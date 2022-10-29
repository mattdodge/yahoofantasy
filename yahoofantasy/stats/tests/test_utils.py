from collections import namedtuple
from unittest import TestCase
from yahoofantasy.stats.utils import get_stat_from_value, get_stat_from_stat_list


# An example of what an API matchup's stat looks like after being parsed
StatResult = namedtuple("StatObj", ["stat_id", "value"])


class TestStatUtils(TestCase):
    def test_missing_leagues(self):
        with self.assertRaises(ValueError):
            get_stat_from_stat_list("R", [StatResult("7", 50)], league_type="nfl")
        with self.assertRaises(ValueError):
            get_stat_from_value(StatResult("7", 50), league_type="xxx")

    def test_get_stat_from_value(self):
        # String stat ID and stat value
        stat = get_stat_from_value(StatResult("60", "65/290"))
        self.assertEqual(stat.display, "H/AB")
        self.assertEqual(stat.value, "65/290")
        # Integer stat ID and stat value
        stat = get_stat_from_value(StatResult(7, 50))
        self.assertEqual(stat.display, "R")
        self.assertEqual(stat.value, 50)

    def test_get_stat_from_stat_list(self):
        stat_list = [
            StatResult("60", "65/290"),  # H/AB
            StatResult("7", 50),  # Hitter Runs
            StatResult("36", 10),  # Pitcher Runs
        ]
        self.assertEqual(get_stat_from_stat_list("H/AB", stat_list), "65/290")
        # Make sure we can get hitter runs and pitcher runs with our order flag
        self.assertEqual(get_stat_from_stat_list("R", stat_list, order=1), 50)
        self.assertEqual(get_stat_from_stat_list("R", stat_list, order=0), 10)
        # Stat missing from stat list
        with self.assertRaises(ValueError):
            get_stat_from_stat_list("HR", stat_list)
        # Non existent stat
        with self.assertRaises(ValueError):
            get_stat_from_stat_list("WAR++", stat_list)
