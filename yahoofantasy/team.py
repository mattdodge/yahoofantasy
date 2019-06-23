from yahoofantasy.api.parse import from_response_object


class Team():

    @staticmethod
    def from_response(resp):
        return from_response_object(Team(), resp)
