from pydantic import BaseModel


class UniversityBase(BaseModel):
    """
    All variables that represent columns in the University table and their data type.
    """
    uni_id: int
    uni_name: str

    model_config: dict = {'from_attributes': True}
