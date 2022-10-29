from time import time
from unittest import TestCase
from unittest.mock import patch, mock_open, ANY
from yahoofantasy.util.persistence import save, load, CURRENT_PERSISTENCE


class TestPersistence(TestCase):
    @patch("yahoofantasy.util.persistence.isfile")
    @patch("yahoofantasy.util.persistence.pickle")
    @patch("builtins.open", new_callable=mock_open)
    def test_persistence(self, m_open, m_pickle, m_isfile):
        """Test a simple persistence flow - save then load"""
        # Pretend there's no persistence file, then save some stuff
        m_isfile.return_value = False
        save("nested.key", "value")
        m_open.assert_called_once_with(".yahoofantasy", "wb")
        m_pickle.dump.assert_called_once_with(
            {
                "nested": {
                    "key": "value",
                    "key__time": ANY,
                },
            },
            m_open.return_value,
        )
        # Make sure we keep track of the saved data in memory
        self.assertEqual(CURRENT_PERSISTENCE["nested"]["key"], "value")
        m_open.reset_mock()
        m_pickle.reset_mock()
        # Now load the data but make sure we grab it from memory and not disk
        loaded_value = load("nested.key")
        self.assertEqual(loaded_value, "value")
        m_open.assert_not_called()
        # Now clear the in memory cache and do it again, we should hit disk this time
        CURRENT_PERSISTENCE.clear()
        m_isfile.return_value = True
        m_pickle.load.return_value = {
            "nested": {
                "key": "value",
                "key__time": time() - 5,
            },
        }
        loaded_value = load("nested.key")
        self.assertEqual(loaded_value, "value")
        m_open.assert_called_once_with(".yahoofantasy", "rb")
        self.assertEqual(CURRENT_PERSISTENCE["nested"]["key"], "value")
        # Now load with an expired TTL
        loaded_value = load("nested.key", default="expired", ttl=0)
        self.assertEqual(loaded_value, "expired")
        # Exception raised if no default present
        with self.assertRaises(ValueError):
            load("nested.key", ttl=0)
        # Now load with disabled TTL
        loaded_value = load("nested.key", default="expired", ttl=-1)
        self.assertEqual(loaded_value, "value")
