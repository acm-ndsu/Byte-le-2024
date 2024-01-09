from pydantic import BaseModel
from datetime import datetime


class RunBase(BaseModel):
    """
    All variables to represent the columns in the Run table and their data type.
    """
    run_id: int
    tournament_id: int
    run_time: datetime
    seed: int
    results: bytes

    model_config: dict = {'from_attributes': True}
