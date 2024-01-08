from pydantic import BaseModel


class SubmissionRunInfoBase(BaseModel):
    """
    All variables that represent columns in the Submission Run Info table and their data type.
    """
    submission_run_info_id: int
    run_id: int
    submission_id: int
    error_txt: str
    player_num: int
    points_awarded: int

    model_config: dict = {'from_attributes': True}
