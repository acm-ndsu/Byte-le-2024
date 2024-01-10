from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload, Query

from server.models.turn import Turn
from server.schemas.turn.turn_schema import TurnBase


# create method for turn
def create(db: Session, turn: TurnBase) -> Turn:
    """
    This method will create an entry in the ``Turn`` table based on the turn.py file. Refer to the
    ``models`` package for more information about turn.py.
    :param db:
    :param turn:
    :return:
    """
    db_turn: Turn = Turn(**turn.model_dump())
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn


# create method that adds the entire list of Turn
def create_all(db: Session, turns: [TurnBase]) -> None:
    inserts: list[Turn] = [Turn(**turn.model_dump()) for turn in turns]
    db.add_all(inserts)
    db.commit()


# read the most recent turn
def read(db: Session, turn_number: int, run_id: int, eager: bool = False) -> Turn | None:
    """
    This gets information from the Turn table and returns it. Eager loading will determine whether to only return the
    entry in the Turn table or to return it with more information from the tables that it's related to.
    :param db:
    :param turn_number:
    :param run_id:
    :param eager:
    :return:
    """
    return (db.query(Turn)
            .filter(and_(Turn.turn_number == turn_number,
                         Turn.run_id == run_id))
            .first() if not eager
            else db.query(Turn)
            .options(joinedload(Turn.run))
            .filter(and_(Turn.turn_number == turn_number,
                         Turn.run_id == run_id))
            .first())


# read all turns
def read_all(db: Session, eager: bool = False) -> [Turn]:
    """
    Returns all Turn entities from the datatable. Eager loading determines whether to return all entities or return all
    entities with information from related tables.
    :param db:
    :param eager:
    :return:
    """
    return (db.query(Turn)
            .all() if not eager
            else db.query(Turn)
            .options(joinedload(Turn.run))
            .all())


# read a specified turn
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Turn]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(Turn)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Turn)
            .options(joinedload(Turn.run))
            .filter_by(**kwargs)
            .all())


# update a turn
def update(db: Session, turn_number: int, run_id: int, turn: TurnBase) -> Turn | None:
    """
    This method takes a Turn object and updates the specified Turn in the database with it. If there is nothing to
    update, returns None.
    :param db:
    :param turn_number:
    :param run_id:
    :param turn:
    :return:
    """
    db_turn: Turn | None = (db.query(Turn)
                            .filter(and_(Turn.turn_number == turn_number,
                                         Turn.run_id == run_id))
                            .one_or_none())
    if db_turn is None:
        return

    for key, value in turn.model_dump().items():
        setattr(db_turn, key, value) if value is not None else None

    db.commit()
    db.refresh(db_turn)
    return db_turn


# delete a turn
def delete(db: Session, turn_number: int, run_id: int) -> None:
    """
    Deletes the specified Turn entity from the database.
    :param db:
    :param turn_number:
    :param run_id:
    :return: None
    """
    db_turn: Turn | None = (db.query(Turn)
                            .filter(and_(Turn.turn_number == turn_number,
                                         Turn.run_id == run_id))
                            .one_or_none())
    if db_turn is None:
        return

    db.delete(db_turn)
    db.commit()


def delete_all(db: Session) -> None:
    """
    Deletes all turn records from the database
    :param db:
    :return: None
    """
    db_turns: Query = db.query(Turn)

    db_turns.delete()
    db.commit()
