from server.schemas.submission.submission_partial import SubmissionSchemaPartial
from server.schemas.team.team_base import TeamBase
from server.schemas.team_type.team_type_schema import TeamTypeBase
from server.schemas.university.university_schema import UniversityBase


# University <-> Team: Many to One
class TeamSchemaPartial(TeamBase):
    """
    Schema for Team using TeamBase and includes its relations. Submission relation is from the SubmissionSchemaPartial
    class since the minimum data from it is needed.
    """
    university: UniversityBase
    team_type: TeamTypeBase
    submissions: list[SubmissionSchemaPartial]
