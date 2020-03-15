from unittest import TestCase
from unittest.mock import patch
from yahoofantasy.api.connection import Connection
# from .sample_responses import make_test_request


class TestConnection(TestCase):

    @patch('yahoofantasy.api.fetch.make_request', return_value={})
    @patch('yahoofantasy.api.parse.from_response_object')
    def test_fetch_no_persist(self, _, mock_request):
        con = Connection(persist=None)
        con.fetch()
        import pdb
        pdb.set_trace()  # XXX BREAKPOINT
        pass
