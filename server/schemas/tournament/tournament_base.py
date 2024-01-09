from pydantic import BaseModel
from datetime import datetime


class TournamentBase(BaseModel):
    """
    All variables that represent columns in the Tournament table and their data type.
    """
    tournament_id: int
    start_run: datetime
    launcher_version: str
    runs_per_client: int
    is_finished: bool

    model_config: dict = {'from_attributes': True}
