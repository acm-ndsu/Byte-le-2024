from sqlalchemy.orm import Session, joinedload

from server.models.team_type import TeamType
from server.schemas.team_type.team_type_schema import TeamTypeBase


# create method for team type
def create(db: Session, team_type: TeamTypeBase) -> TeamType:
    """
    This method will create an entry in the ``Team Type`` table based on the team_type.py file. Refer to the
    ``models`` package for more information about team_type.py.
    :param db:
    :param team_type:
    :return:
    """
    db_team_type: TeamType = TeamType(**team_type.model_dump(exclude={'team_type_id'}))
    db.add(db_team_type)
    db.commit()
    db.refresh(db_team_type)
    return db_team_type


# read most recent team type
def read(db: Session, id: int, eager: bool = False) -> TeamType | None:
    """
    This gets information from the Team Type table and returns it. Eager loading will determine whether to only return
    the entry in the Team Type table or to return it with more information from the tables that it's related to.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    return (db.query(TeamType)
            .filter(TeamType.team_type_id == id)
            .first() if not eager
            else db.query(TeamType)
            .options(joinedload(TeamType.teams))
            .filter(TeamType.team_type_id == id)
            .first())


# read all team types
def read_all(db: Session, eager: bool = False) -> [TeamType]:
    """
    Returns all Team Type entities from the datatable. Eager loading determines whether to return all entities or return
    all entities with information from related tables.
    :param db:
    :param eager:
    :return:
    """
    return (db.query(TeamType)
            .all() if not eager
            else db.query(TeamType)
            .options(joinedload(TeamType.teams))
            .all())


# read specified team type
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [TeamType]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(TeamType)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(TeamType)
            .options(joinedload(TeamType.teams))
            .filter_by(**kwargs)
            .all())


# update a team type
def update(db: Session, id: int, team_type: TeamTypeBase) -> TeamType | None:
    """
    This method takes a Team Type object and updates the specified Team Type in the database with it. If there is
    nothing to update, returns None.
    :param db:
    :param id:
    :param team_type:
    :return:
    """
    db_team_type: TeamType | None = (db.query(TeamType)
                                     .filter(TeamType.team_type_id == id)
                                     .one_or_none())
    if db_team_type is None:
        return

    for key, value in team_type.model_dump().items():
        setattr(db_team_type, key, value) if value is not None else None

    db.commit()
    db.refresh(db_team_type)
    return db_team_type


# delete a team type
def delete(db: Session, id: int, team_type: TeamTypeBase) -> None:
    """
    Deletes the specified Team Type entity from the database.
    :param db:
    :param id:
    :param team_type:
    :return: None
    """
    db_team_type: TeamType | None = (db.query(TeamType)
                                     .filter(TeamType.team_type_id == id)
                                     .one_or_none())
    if db_team_type is None:
        return

    db.delete(db_team_type)
    db.commit()
