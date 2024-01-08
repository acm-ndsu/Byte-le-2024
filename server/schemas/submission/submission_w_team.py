from server.schemas.submission.submission_base import SubmissionBase


class SubmissionWTeam(SubmissionBase):
    """
    Schema for Submission using SubmissionBase and includes team_uuid. Separated the team uuid to protect it. Only the
    team that owns the uuid should be able to access their submission data.
    """
    team_uuid: str
    