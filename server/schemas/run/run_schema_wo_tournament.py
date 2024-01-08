from __future__ import annotations

from server.schemas.run.run_base import RunBase
from server.schemas.submission_run_info.submission_run_info_w_submission import SubmissionRunInfoWSubmission
from server.schemas.turn.turn_schema import TurnBase


class RunSchemaWithoutTournament(RunBase):
    """
    Schema for Run using RunBase. Includes its relations to other tables EXCEPT tournament.
    """
    submission_run_infos: list[SubmissionRunInfoWSubmission]
