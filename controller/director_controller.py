from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.director_model import Director
from schema.director_schema import DirectorCreate, DirectorUpdate


def get_all(db:Session, skip:int=0, limit:int=100)-> List[Director]:
    try:
        return db.query(Director).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in playing the director {str(error)}"
        )

def create_director(db:Session, director_data: DirectorCreate) -> Director:

    new_director = Director(
        name = director_data.name,
        biography = director_data.biography,
    )

    try:
        db.add(new_director)
        db.commit()
        db.refresh(new_director)
        return new_director
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in playing the movie {str(error)}"
        )

def get_by_id(db: Session, director_id: int) -> Director:
    try:
        director = db.query(Director).filter(Director.id == director_id).first()
        if not director:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Director with id {director_id} not found"
            )
        return director
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching director: {str(error)}"
        )

def update_director(db: Session, director_id: int, director_data: DirectorUpdate) -> Director:
    db_director = get_by_id(db, director_id)

    update_data = director_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_director, field, value)

    try:
        db.commit()
        db.refresh(db_director)
        return db_director
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating director: {str (error)}"
        )

def delete_director(db: Session, director_id: int) -> dict:
    db_director = get_by_id(db, director_id)

    try:
        db.delete(db_director)
        db.commit()
        return {"message": f"Director with id {director_id} deleted successfully"}
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting director: {str(error)}"
        )