from yahoofantasy.resources.player import Player


class DraftResult:
    def __init__(self, league, team):
        self.league = league
        self.team = team

    # Properties
    #  * pick (int) - The overall pick num
    #  * round (int) - The round of the draft pick, starts at 1

    @property
    def player(self):
        return Player.from_response(self.players.player.__dict__, self.league)

    def __repr__(self):
        return f"Round {self.round} Pick {self.pick} - {self.player.name.full} by {self.team.manager.nickname}"
