
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from model.movie_model import Movie
from model.director_model import Director
from model.genre_model import Genre
from schema.movie_schema import MovieCreate, MovieUpdate


def get_all(db:Session, skip:int=0, limit:int=100)-> List[Movie]:
    try:
        return db.query(Movie).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in playing the movie {str(error)}"
        )

def create_movie(db:Session, movie_data: MovieCreate) -> Movie:

    if movie_data.director_id is not None:
        director_exists = db.get(Director, movie_data.director_id)
        if director_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Director with id {movie_data.director_id} does not exist"
            )

    genres = []
    if movie_data.genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(movie_data.genre_ids)).all()
        found = {genre.id for genre in genres}
        missing = [gid for gid in movie_data.genre_ids if gid not in found]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with ids {missing} does not exist"
            )

    new_movie = Movie(
        title=movie_data.title,
        director_id=movie_data.director_id,
        duration=movie_data.duration,
        year=movie_data.year,
        is_available=movie_data.is_available
    )

    if genres:
        new_movie.genres = genres

    try:
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        return new_movie
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail=f"Invalid data for movie: {getattr(error, 'orig', error)}"
        )
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in finding the movie {str(error)}"
        )

def get_by_id(db: Session, movie_id: int) -> Movie:
    try:
        movie = db.query(Movie).filter(Movie-id == movie_id).first()
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found"
            )
        return movie
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error fetching movie: {str(error)}"
        )

def update_movie(db: Session, movie_id: int, movie_data: MovieUpdate) -> Movie:
    db_movie = get_by_id(db, movie_id)
    
    update_data = movie_data.model_dump(exclude_unset=True)

    if "director_id" in update_data and update_data["director_id"] is not None:
        director_exists = db.get(Director, update_data["director_id"])
        if director_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Director with ID {update_data['director_id']} does not exist"
            )

    if "genre_ids" in update_data:
        genre_ids = update_data.pop("genre_ids")
        if genre_ids:
            genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            found = {genre.id for genre in genres}
            missing = [gid for gid in genre_ids if gid not in found]
            if missing:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Genre with ID's {missing} does not exist"
                )
            db_movie.genres = genres
        else:
            db_movie.genres = []

    for field, value in update_data.items():
        setattr(db_movie, field, value)

    try:
        db.commit()
        db.refresh(db_movie)
        return db_movie
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid data for movie: {getattr(error, 'orig', error)}"
        )
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error updating movie: {str(error)}"
        )

def delete_movie(db: Session, movie_id: int) -> dict:

    db_movie = get_by_id(db, movie_id)

    try:
        db.delete(db_movie)
        db.commit()
        return {"message": f"Movie with ID {movie_id} deleted succesfully"}
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting movie: {str(error)}"
        )