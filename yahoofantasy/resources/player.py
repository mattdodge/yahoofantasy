from yahoofantasy.api.parse import from_response_object


class Player():

    @staticmethod
    def from_response(resp):
        return from_response_object(Player(), resp)
