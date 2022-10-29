import pydash as _
from yahoofantasy.api.parse import from_response_object, as_list
from .team import Team


# A player involved in a transaction
class TransactionPlayer:
    def __init__(self, transaction):
        self.transaction = transaction

    @property
    def from_team(self):
        if self.transaction_data.source_type == "team":
            team = Team(
                self.transaction.league.ctx,
                self.transaction.league,
                self.transaction_data.source_team_key,
            )
            setattr(team, "name", self.transaction_data.source_team_name)
            return team
        return self.transaction_data.source_type

    @property
    def to_team(self):
        if self.transaction_data.destination_type == "team":
            team = Team(
                self.transaction.league.ctx,
                self.transaction.league,
                self.transaction_data.destination_team_key,
            )
            setattr(team, "name", self.transaction_data.destination_team_name)
            return team
        return self.transaction_data.destination_type

    def __repr__(self):
        return f"{self.transaction_data.type} {self.name.full} from {self.from_team} to {self.to_team}"


class Transaction:
    def __init__(self, league):
        self.league = league
        self.involved_players = []

    # Properties
    #  * type (str) - The overall type of transaction (e.g., 'add/drop')
    #  * status (str) - The result of the transaction (e.g., 'successful')
    #  * timestamp (int) - The unix timestamp the transaction was processed
    #  * faab_bid (int) - The amount of FAAB spent (if applicable)

    @staticmethod
    def from_response(resp, league):
        trans = from_response_object(Transaction(league), resp)
        for player in as_list(_.get(trans, "players.player", [])):
            tp = TransactionPlayer(trans)
            from_response_object(tp, player.__dict__)
            trans.involved_players.append(tp)
        return trans

    def __repr__(self):
        return f"Transaction {self.type}"
