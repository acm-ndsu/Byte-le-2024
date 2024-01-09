from sqlalchemy.orm import Session, joinedload

from server.models.submission_run_info import SubmissionRunInfo
from server.schemas.submission_run_info.submission_run_info_schema import SubmissionRunInfoBase


# create submission run info
def create(db: Session, submission_run_info: SubmissionRunInfoBase) -> SubmissionRunInfo:
    """
    This method will create an entry in the ``SubmissionRunInfo`` table based on the submission_run_info.py file.
    Refer to the ``models`` package for more information about submission_run_info.py.
    :param db:
    :param submission_run_info:
    :return: SubmissionRunInfo
    """
    db_submission_run_info: SubmissionRunInfo = SubmissionRunInfo(**submission_run_info.model_dump(
        exclude={'submission_run_info_id'}))
    db.add(db_submission_run_info)
    db.commit()
    db.refresh(db_submission_run_info)
    return db_submission_run_info


# read most recent submission run info
def read(db: Session, id: int, eager: bool = False) -> SubmissionRunInfo | None:
    """
    This gets information from the SubmissionRunInfo table and returns it. Eager loading will determine whether to only
    return the entry in the SubmissionRunInfo table or to return it with more information from the tables that it's
    related to.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    return (db.query(SubmissionRunInfo)
            .filter(SubmissionRunInfo.submission_run_info_id == id)
            .first() if not eager
            else db.query(SubmissionRunInfo)
            .options(joinedload(SubmissionRunInfo.submission),
                     joinedload(SubmissionRunInfo.run))
            .filter(SubmissionRunInfo.submission_run_info_id == id)
            .first())


# read all submission run info
def read_all(db: Session, eager: bool = False) -> [SubmissionRunInfo]:
    """
    Returns all SubmissionRunInfo entities from the datatable. Eager loading determines whether to return all entities
    or return all entities with information from related tables.
    :param db:
    :param eager:
    :return:
    """
    return (db.query(SubmissionRunInfo)
            .all() if not eager
            else db.query(SubmissionRunInfo)
            .options(joinedload(SubmissionRunInfo.submission),
                     joinedload(SubmissionRunInfo.run))
            .all())


# read specified submission run info
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [SubmissionRunInfo]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(SubmissionRunInfo)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(SubmissionRunInfo)
            .options(joinedload(SubmissionRunInfo.submission),
                     joinedload(SubmissionRunInfo.run))
            .filter_by(**kwargs)
            .all())


# update a submission run info
def update(db: Session, id: int, submission_run_info: SubmissionRunInfoBase) -> SubmissionRunInfo | None:
    """
    This method takes a SubmissionRunInfo object and updates the specified SubmissionRunInfo in the database with it.
    If there is nothing to update, returns None.
    :param db:
    :param id:
    :param submission_run_info:
    :return:
    """
    db_submission_run_info: SubmissionRunInfo | None = (db.query(SubmissionRunInfo)
                                                        .filter(SubmissionRunInfo.submission_run_info_id == id)
                                                        .one_or_none())
    if db_submission_run_info is None:
        return

    for key, value in submission_run_info.model_dump().items():
        setattr(db_submission_run_info, key, value) if value is not None else None

    db.commit()
    db.refresh(db_submission_run_info)
    return db_submission_run_info


# delete a submission run info
def delete(db: Session, id: int, submission_run_info: SubmissionRunInfoBase) -> None:
    """
    Deletes the specified SubmissionRunInfo entity from the database.
    :param db:
    :param id:
    :param submission_run_info:
    :return: None
    """
    db_submission_run_info: SubmissionRunInfo | None = (db.query(SubmissionRunInfo)
                                                        .filter(SubmissionRunInfo.submission_run_info_id == id)
                                                        .one_or_none())
    if db_submission_run_info is None:
        return

    db.delete(db_submission_run_info)
    db.commit()
