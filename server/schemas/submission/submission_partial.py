from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.team.team_base import TeamBase


class SubmissionSchemaPartial(SubmissionBase):
    """
    Schema for Submission using SubmissionBase and includes its relation to team.
    """
    team: TeamBase
