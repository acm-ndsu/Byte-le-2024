from server.schemas.team.team_base import TeamBase


class TeamIdSchema(TeamBase):
    """
    Schema for TeamId using TeamBase. Separated from everything else to protect the uuid.
    """
    team_uuid: str
