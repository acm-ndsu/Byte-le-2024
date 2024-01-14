from pydantic import BaseModel


class TurnBase(BaseModel):
    """
    All variables that represent columns in the Turn table and their data type.
    """
    turn_number: int
    run_id: int
    turn_data: bytes

    model_config: dict = {'from_attributes': True}
