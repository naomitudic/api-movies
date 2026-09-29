
from typing import List
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from database.database import get_db
from schema.movie_schema import MovieCreate, MovieResponse, MovieUpdate
import controller.movie_controller as controller

router = APIRouter(
    prefix="/movie",
    tags=["Movie"]
)

@router.get(
    "/",
    response_model=List[MovieResponse],
    summary="All movies",
    description="See all movies"
)
def watch_movies(
    skip:int = Query(0, ge=0, description="Number record"),
    limit:int = Query(100, ge=1, le=100, description="Number record"),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)

@router.get(
        "/{movie_id}",
        response_model=MovieResponse,
        summary="Get movie by ID",
        description="Fetch a specific movie by its ID"
)
def watch_movie(
    movie_id: int = Path(..., ge=1, description="The movie's ID"),
    db: Session = Depends(get_db)
):
    return controller.get_by_id(db=db, movie_id=movie_id)


@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new movie",
    description="Upload a new movie"
)
def create_new_movie(
    movie_data: MovieCreate,
    db:Session=Depends(get_db)
):
    return controller.create_movie(db=db, movie_data=movie_data)

@router.put(
    "/{movie_id}",
    response_model=MovieResponse,
    summary="Update a movie",
    description="Update an existing movie's details or relationships by ID"
)
def update_existing_movie(
    movie_data: MovieUpdate,
    movie_id: int = Path(..., ge=1, description="The movie's ID to update"),
    db: Session = Depends(get_db)
):
    return controller.update_movie(db=db, movie_id=movie_id, movie_data=movie_data)

@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a movie",
    description="Delete a movie by its ID"
)
def delete_existing_movie(
    movie_id: int = Path(..., ge=1, description="The movie's ID to delete"),
    db: Session = Depends(get_db)
):
    return controller.delete_movie(db=db, movie_id=movie_id)