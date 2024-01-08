from sqlalchemy.orm import Session, joinedload

from server.models.team import Team
from server.schemas.team.team_schema import TeamBase


# create method for team
def create(team: TeamBase, db: Session) -> Team:
    """
    This method will create a table in the database called ``Team`` based on the run.py class. Refer to the ``models``
    package for more information on them.
    :param team:
    :param db:
    :return:
    """
    db_team: Team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


# read most recent team
def read(db: Session, id: int, eager: bool = False) -> Team | None:
    """
    This method will create an entry in the ``Team`` table based on the team.py file. Refer to the
    ``models`` package for more information about team.py.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    return (db.query(Team)
            .filter(Team.team_uuid == id)
            .first() if not eager
            else db.query(Team)
            .options(joinedload(Team.university),
                     joinedload(Team.team_type),
                     joinedload(Team.submissions))
            .filter(Team.team_uuid == id)
            .first())


# read all teams
def read_all(db: Session, eager: bool = False) -> [Team]:
    """
    Returns all Team entities from the datatable. Eager loading determines whether to return all entities or return all
    entities with information from related tables.
    :param db:
    :param eager:
    :return:
    """
    return (db.query(Team)
            .all() if not eager
            else db.query(Team)
            .options(joinedload(Team.university),
                     joinedload(Team.team_type),
                     joinedload(Team.submissions))
            .all())


# read a specified team
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Team]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(Team)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Team)
            .options(joinedload(Team.university),
                     joinedload(Team.team_type),
                     joinedload(Team.submissions))
            .all())


# update a team
def update(db: Session, id: int, team: TeamBase) -> Team | None:
    """
    This method takes a Team object and updates the specified Team in the database with it. If there is nothing to
    update, returns None.
    :param db:
    :param id:
    :param team:
    :return:
    """
    db_team: Team | None = (db.query(Team)
                            .filter(Team.team_uuid == id)
                            .one_or_none())
    if db_team is None:
        return

    for key, value in team.model_dump().items():
        setattr(db_team, key, value) if value is not None else None

    db.commit()
    db.refresh(db_team)
    return db_team


# delete a team
def delete(db: Session, id: int, team: TeamBase) -> None:
    """
    Deletes the specified Team entity from the database.
    :param db:
    :param id:
    :param team:
    :return:
    """
    db_team: Team | None = (db.query(Team)
                                        .filter(Team.team_uuid == id)
                                        .one_or_none())
    if db_team is None:
        return

    db.delete(db_team)
    db.commit()
