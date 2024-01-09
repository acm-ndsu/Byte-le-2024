from sqlalchemy.orm import Session, joinedload

from server.models.university import University
from server.schemas.university.university_schema import UniversityBase


# create method for university
def create(db: Session, university: UniversityBase) -> University:
    """
    This method will create an entry in the ``University`` table based on the university.py file. Refer to the
    ``models`` package for more information about university.py.
    :param db:
    :param university:
    :return:
    """
    db_university: University = University(**university.model_dump(exclude={'uni_id'}))
    db.add(db_university)
    db.commit()
    db.refresh(db_university)
    return db_university


# read most recent university
def read(db: Session, id: int, eager: bool = False) -> University | None:
    """
    This gets information from the University table and returns it. Eager loading will determine whether to only return
    the entry in the University table or to return it with more information from the tables that it's related to.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    return (db.query(University)
            .filter(University.uni_id == id)
            .first() if not eager
            else db.query(University)
            .options(joinedload(University.teams))
            .filter(University.uni_id == id)
            .first())


# read all universities
def read_all(db: Session, eager: bool = False) -> [University]:
    """
    Returns all University entities from the datatable. Eager loading determines whether to return all entities or
    return all entities with information from related tables.
    :param db:
    :param eager:
    :return:
    """
    return (db.query(University)
            .all() if not eager
            else db.query(University)
            .options(joinedload(University.teams))
            .all())


# read specified university
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [University]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(University)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(University)
            .options(joinedload(University.teams))
            .filter_by(**kwargs)
            .all())


# update a university
def update(db: Session, id: int, university: UniversityBase) -> University | None:
    """
    This method takes a University object and updates the specified University in the database with it. If there is
    nothing to update, returns None.
    :param db:
    :param id:
    :param university:
    :return:
    """
    db_university: University | None = (db.query(University)
                                        .filter(University.uni_id == id)
                                        .one_or_none())
    if db_university is None:
        return

    for key, value in university.model_dump().items():
        setattr(db_university, key, value) if value is not None else None

    db.commit()
    db.refresh(db_university)
    return db_university


# delete a university
def delete(db: Session, id: int, university: UniversityBase) -> None:
    """
    Deletes the specified University entity from the database.
    :param db:
    :param id:
    :param university:
    :return: None
    """
    db_university: University | None = (db.query(University)
                                        .filter(University.uni_id == id)
                                        .one_or_none())
    if db_university is None:
        return

    db.delete(db_university)
    db.commit()
