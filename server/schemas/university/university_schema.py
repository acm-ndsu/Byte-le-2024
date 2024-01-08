from server.schemas.team.team_base import TeamBase
from server.schemas.university.university_base import UniversityBase


# University <-> Team: Many to One
class UniversitySchema(UniversityBase):
    """
    Schema for University using UniversityBase. Includes its relations.
    """
    teams: list[TeamBase]
