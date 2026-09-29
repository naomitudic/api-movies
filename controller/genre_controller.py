from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from model.genre_model import Genre
from schema.genre_schema import GenreCreate, GenreUpdate


def get_all(db:Session, skip:int=0, limit:int=100)-> List[Genre]:
    try:
        return(
            db.query(Genre)
            .options(joinedload(Genre.movies))
            .offset(skip)
            .limit(limit)
            .all()
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching genres {str(error)}"
        )

def create_genre(db:Session, genre_data: GenreCreate) -> Genre:

    existing_genre = db.query(Genre).filter(Genre.name == genre_data.name).first()
    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Genre with name '{genre_data.name}' already exist"
        )

    new_genre = Genre(name = genre_data.name)

    try:
        db.add(new_genre)
        db.commit()
        db.refresh(new_genre)
        return new_genre
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating genre {str(error)}"
        )

def get_by_id(db: Session, genre_id: int) -> Genre:
    try:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with ID {genre_id} not found"
            )
        return genre
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching genre: {str(error)}"
        )

def update_genre(db: Session, genre_id: int, genre_data: GenreUpdate) -> Genre:
    db_genre = get_by_id(db, genre_id)

    update_data = genre_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_genre, field, value)

    try:
        db.commit()
        db.refresh(db_genre)
        return db_genre
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating genre: {str (error)}"
        )

def delete_genre(db: Session, genre_id: int) -> dict:
    db_genre = get_by_id(db, genre_id)

    try:
        db.delete(db_genre)
        db.commit()
        return {"message": f"Genre with ID {genre_id} deleted successfully"}
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting genre: {str(error)}"
        )