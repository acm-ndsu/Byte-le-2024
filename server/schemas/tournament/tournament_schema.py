from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.run.run_schema_wo_tournament import RunSchemaWithoutTournament


class TournamentSchema(TournamentBase):
    """
    Schema for Tournament using TournamentBase. Includes its relations.
    """
    runs: list[RunSchemaWithoutTournament]
