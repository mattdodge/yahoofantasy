from yahoofantasy.api.parse import from_response_object


class Player():

    @staticmethod
    def from_response(resp):
        return from_response_object(Player(), resp)

    def __repr__(self):
        try:
            return f"Player: {self.names.full} ({self.display_position} - {self.editorial_team_abbr})"
        except AttributeError:
            return "Player: Unknown Player"
