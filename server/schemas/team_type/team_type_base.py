from pydantic import BaseModel


class TeamTypeBase(BaseModel):
    """
    All variables that represent columns in the Team Type table and their data type.
    """
    team_type_id: int
    team_type_name: str
    eligible: bool

    model_config: dict = {'from_attributes': True}
