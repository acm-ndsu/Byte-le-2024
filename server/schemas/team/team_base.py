from pydantic import BaseModel


class TeamBase(BaseModel):
    """
    All variables that represent columns in the Team table and their data type.
    """
    uni_id: int
    team_type_id: int
    team_name: str

    model_config: dict = {'from_attributes': True}
