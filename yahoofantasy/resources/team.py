from yahoofantasy.api.parse import as_list


class Team():

    def __init__(self, ctx, league, team_id):
        self.ctx = ctx
        self.league = league
        self.id = team_id

    @property
    def manager(self):
        """ We can have multiple managers, so here's a shortcut to get 1 manager """
        return as_list(self.managers.manager)[0]
