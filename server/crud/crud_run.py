from sqlalchemy.orm import Session, joinedload

from server.models.run import Run
from server.schemas.run.run_schema import RunBase


# Create method for Run
def create(db: Session, run: RunBase) -> Run:
    """
    This method will create an entry in the ``Run`` table based on the run.py file. Refer to the ``models``
    package for more information about the run.py.
    :param db:
    :param run:
    :return: Run
    """
    db_run: Run = Run(**run.model_dump(exclude={'run_id'}))
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


# read the most recent run
def read(db: Session, id: int, eager: bool = False) -> Run | None:
    """
    This gets information from the Run table and returns it. Eager loading will determine whether to only return the
    entry in the Run table or to return it with more information from the tables that it's related to.
    :param db:
    :param id:
    :param eager:
    :return: Run | None
    """
    return (db.query(Run)
            .filter(Run.run_id == id)
            .first() if not eager
            else db.query(Run)
            .options(joinedload(Run.turns),
                     joinedload(Run.submission_run_infos),
                     joinedload(Run.tournament))
            .filter(Run.run_id == id)
            .first())


# read all runs
def read_all(db: Session, eager: bool = False) -> [Run]:
    """
    Returns all Run entities from the datatable. Eager loading determines whether to return all entities or return all
    entities with information from related tables.
    :param db:
    :param eager:
    :return: a list of Run objects
    """
    return db.query(Run).all() if not eager \
        else db.query(Run).options(joinedload(Run.turns),
                                   joinedload(Run.submission_run_infos),
                                   joinedload(Run.tournament)).all()


# read a specified run
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Run]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return: a list of Run objects
    """
    return (db.query(Run)
            .filter_by(**kwargs)
            .all() if not eager else
            db.query(Run)
            .options(joinedload(Run.turns),
                     joinedload(Run.submission_run_infos),
                     joinedload(Run.tournament))
            .filter_by(**kwargs).all())


# Update a run
def update(db: Session, id: int, run: RunBase) -> Run | None:
    """
    This method takes a Run object and updates the specified Run in the database with it. If there is nothing to
    update, returns None.
    :param db:
    :param id:
    :param run:
    :return: a Run object or None
    """
    db_run: Run | None = (db.query(Run)
                          .filter(Run.run_id == id)
                          .one_or_none())
    if db_run is None:
        return

    for key, value in run.model_dump().items():
        setattr(db_run, key, value) if value is not None else None

    db.commit()
    db.refresh(db_run)
    return db_run


# delete a run
def delete(db: Session, id: int, run: RunBase) -> None:
    """
    Deletes the specified Run entity from the database.
    :param db:
    :param id:
    :param run:
    :return: None
    """
    db_run: Run | None = (db.query(Run)
                          .filter(Run.run_id == id)
                          .one_or_none())
    if db_run is None:
        return

    db.delete(db_run)
    db.commit()
