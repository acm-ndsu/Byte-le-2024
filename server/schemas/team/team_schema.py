from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.team.team_base import TeamBase
from server.schemas.team_type.team_type_schema import TeamTypeBase
from server.schemas.university.university_schema import UniversityBase


# University <-> Team: Many to One
class TeamSchema(TeamBase):
    """
    Schema for Team using TeamBase. Includes its relations.
    """
    university: UniversityBase
    team_type: TeamTypeBase
    submissions: list[SubmissionBase]
