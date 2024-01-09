from pydantic import BaseModel
from datetime import datetime


class SubmissionBase(BaseModel):
    """
    All variables to represent the columns in the Submission table and their data type.
    """
    submission_id: int
    submission_time: datetime
    file_txt: bytes

    model_config: dict = {'from_attributes': True}
