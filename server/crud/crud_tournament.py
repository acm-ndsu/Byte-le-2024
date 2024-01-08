from sqlalchemy.orm import Session, joinedload

from server.models.run import Run
from server.models.submission import Submission
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.tournament import Tournament
from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.tournament.tournament_schema import TournamentSchema


# create method for tournament
def create(db: Session, tournament: TournamentBase) -> Tournament:
    """
    This method will create a table in the database called ``Tournament`` based on the run.py class. Refer to the
    ``models`` package for more information on them.
    :param db:
    :param tournament:
    :return:
    """
    db_tournament: Tournament = Tournament(**tournament.model_dump(exclude={'tournament_id'}))
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


# read most recent tournamet
def read(db: Session, id: int, eager: bool = False) -> Tournament | None:
    """
    This method will create an entry in the ``Tournament`` table based on the tournament.py file. Refer to the
    ``models`` package for more information about tournament.py.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    return (db.query(Tournament)
            .filter(Tournament.tournament_id == id)
            .first() if not eager
            else db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team))
            .filter(Tournament.tournament_id == id)
            .first())


# read all tournaments
def read_all(db: Session, eager: bool = False) -> [Tournament]:
    """
    Returns all Tournament entities from the datatable. Eager loading determines whether to return all entities or
    return all entities with information from related tables.
    :param db:
    :param eager:
    :return:
    """
    return (db.query(Tournament)
            .order_by(Tournament.start_run.desc())
            .all() if not eager
            else db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team))
            .order_by(Tournament.start_run.desc())
            .all())


# read specified tournament
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Tournament]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(Tournament)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team))
            .filter_by(**kwargs)
            .all())


# update a tournament
def update(db: Session, id: int, tournament: TournamentBase) -> Tournament | None:
    """
    This method takes a Tournament object and updates the specified Tournament in the database with it. If there is
    nothing to update, returns None.
    :param db:
    :param id:
    :param tournament:
    :return:
    """
    db_tournament: Tournament | None = (db.query(Tournament)
                                        .filter(Tournament.tournament_id == id)
                                        .one_or_none())
    if db_tournament is None:
        return

    for key, value in tournament.model_dump().items():
        setattr(db_tournament, key, value) if value is not None else None

    db.commit()
    db.refresh(db_tournament)
    return db_tournament


# delete a tournament
def delete(db: Session, id: int) -> None:
    """
    Deletes the specified Tournament entity from the database.
    :param db:
    :param id:
    :return: None
    """
    db_tournament: Tournament | None = (db.query(Tournament)
                                        .filter(Tournament.tournament_id == id)
                                        .one_or_none())
    if db_tournament is None:
        return

    db.delete(db_tournament)
    db.commit()


def get_latest_tournament(db: Session) -> Tournament | None:
    return (db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team))
            .order_by(Tournament.tournament_id.desc())
            .first())
