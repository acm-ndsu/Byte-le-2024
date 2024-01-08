from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission_run_info.submission_run_info_w_run import SubmissionRunInfoWRun
from server.schemas.team.team_base import TeamBase


class SubmissionSchema(SubmissionBase):
    """
    Schema for Submission using SubmissionBase and includes all its relations.
    """
    team: TeamBase
    submission_run_infos: list[SubmissionRunInfoWRun]
