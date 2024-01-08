from server.schemas.run.run_base import RunBase
from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase


class SubmissionRunInfoSchema(SubmissionRunInfoBase):
    """
    Schema for Submission Run Info using SubmissionRunInfoBase. Includes its relations.
    """
    run: RunBase
    submission: SubmissionBase
